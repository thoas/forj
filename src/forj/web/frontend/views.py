from datetime import datetime

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import generic
from django.conf import settings
from django.contrib.auth import login
from django.db import transaction
from django.utils.functional import cached_property
from django.urls import NoReverseMatch
from django.utils.module_loading import import_string
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone

from forj.web.frontend.forms import RegistrationForm
from forj.models import Order, ContentNode
from forj.cart import Cart
from forj import exceptions
from forj.encoders import JSONEncoder
from forj.payment import backend


headers = (
    "HTTP_HOST",
    "REMOTE_ADDR",
    "HTTP_X_FORWARDED_FOR",
    "HTTP_X_FORWARDED_PROTO",
    "HTTP_X_FORWARDED_PROTOCOL",
    "HTTP_ACCEPT_LANGUAGE",
    "QUERY_STRING",
    "X-Real-Ip",
)


@csrf_exempt
def healthcheck(request):
    user = getattr(request, "user", None)

    results = {header: request.META.get(header) for header in headers}

    results["GET"] = request.GET
    results["POST"] = request.POST
    results["USER"] = "{}".format(user or "")
    results["HOST"] = request.get_host()
    results["IS_SECURE"] = request.is_secure()
    results["IS_AJAX"] = request.is_ajax()

    release_tag = getattr(settings, "RELEASE_TAG", None)

    version = getattr(settings, "PROJECT_VERSION", None)

    uptime = getattr(settings, "PROJECT_UPTIME", None)

    if version is not None and "." in version:
        version = import_string(version)

    results["sha"] = release_tag
    results["tznow"] = timezone.now()
    results["now"] = datetime.now()
    results["version"] = version
    results["uptime"] = uptime
    results["uptime_since"] = naturaltime(uptime)

    return JsonResponse(results)


def home(request, template_name="forj/home.html", **extra):
    extra["nodes"] = {
        "carousel_top": ContentNode.objects.type(
            ContentNode.TYPE_CHOICES.HOME_CAROUSEL_TOP
        ),
        "carousel_bottom": ContentNode.objects.type(
            ContentNode.TYPE_CHOICES.HOME_CAROUSEL_BOTTOM
        ),
        "portrait": ContentNode.objects.type(ContentNode.TYPE_CHOICES.HOME_PORTRAIT),
    }

    return render(request, template_name, extra)


def collection(request, template_name="forj/collection.html", **extra):
    extra["nodes"] = {
        "carousel": ContentNode.objects.type(
            ContentNode.TYPE_CHOICES.COLLECTION_CAROUSEL
        ),
        "selection": ContentNode.objects.type(
            ContentNode.TYPE_CHOICES.COLLECTION_SELECTION
        ),
    }

    return render(request, template_name, extra)


class CheckoutMixin(object):
    @cached_property
    def cart(self):
        return Cart.from_request(self.request)

    @cached_property
    def order(self):
        reference = self.kwargs.get("reference")

        if reference and self.request.user.is_authenticated:
            return Order.objects.filter(
                user=self.request.user, reference=reference
            ).first()

        return None


class CheckoutView(CheckoutMixin, generic.FormView):
    template_name = "forj/checkout/home.html"
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = self.cart

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["country"] = settings.DEFAULT_COUNTRY
        kwargs["order"] = self.order

        return kwargs

    def dispatch(self, *args, **kwargs):
        if not self.cart:
            return redirect("home")

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            self.order = self.cart.save(
                order=self.order,
                defaults={
                    "shipping_address": form.shipping_address,
                    "billing_address": form.billing_address,
                },
            )

            form.save(self.order)

            self.request.session["_order_id"] = self.order.pk

        return super().form_valid(form)

    def get_success_url(self):
        return self.order.get_payment_url()


class OrderView(generic.DetailView):
    slug_field = "reference"
    context_object_name = "order"
    slug_url_kwarg = "reference"

    def get_queryset(self):
        return Order.objects.all()


class PaymentView(OrderView):
    template_name = "forj/checkout/payment.html"

    def get(self, request, *args, **kwargs):
        order = self.get_object()

        if order.is_status_succeeded():
            return redirect(order.get_success_url())

        order = backend.handle_order(order)

        if order.redirect_url:
            return redirect(order.redirect_url)

        if order.is_status_succeeded():
            return redirect(order.get_success_url())

        return super().get(request, *args, **kwargs)


class SuccessView(OrderView):
    template_name = "forj/checkout/success.html"

    def get_queryset(self):
        return super().get_queryset().filter(status=Order.STATUS_CHOICES.SUCCEEDED)


class InvoiceView(SuccessView):
    template_name = "forj/checkout/invoice.html"


@csrf_exempt
def cart(request):
    params = getattr(request, request.method)

    action = params.get("action")

    cart = Cart.from_request(request)
    if cart is None:
        cart = Cart()

    reference_list = params.getlist("reference")

    if action is not None:
        if action == "detail":
            if reference_list is None:
                return HttpResponseBadRequest("Missing `reference` parameter")

            cart = Cart()
            for reference in reference_list:
                try:
                    cart.add_product(reference, params.get("quantity") or 1)
                except exceptions.InvalidProductRef as e:
                    return HttpResponseBadRequest(e)
            return JsonResponse(cart.response, encoder=JSONEncoder)
        elif action in ("add", "remove"):
            if reference_list is None:
                return HttpResponseBadRequest("Missing `reference` parameter")

            try:
                if action == "add":
                    for reference in reference_list:
                        cart.add_product(reference, params.get("quantity") or 1)
                elif action == "remove":
                    for reference in reference_list:
                        cart.remove_product(reference)
            except exceptions.InvalidProductRef as e:
                return HttpResponseBadRequest(e)
        elif action == "flush":
            cart = Cart.flush(request)

        cart.to_request(request)

    next_value = params.get("next")
    if next_value:
        try:
            return redirect(next_value)
        except NoReverseMatch:
            return HttpResponseBadRequest()

    return JsonResponse(cart.response, encoder=JSONEncoder)
