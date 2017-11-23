from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import generic
from django.conf import settings
from django.contrib.auth import login
from django.db import transaction
from django.utils.functional import cached_property
from django.urls import NoReverseMatch

from forj.web.frontend.forms import RegistrationForm
from forj.models import Order, Product
from forj.cart import Cart
from forj import exceptions
from forj.encoders import JSONEncoder


def home(request, template_name='forj/home.html'):
    return render(request, template_name)


def collection(request, template_name='forj/collection.html'):
    return render(request, template_name)


class CheckoutMixin(object):
    @cached_property
    def cart(self):
        return Cart.from_request(self.request)

    @cached_property
    def order(self):
        reference = self.kwargs.get('reference')

        if reference and self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user,
                                        reference=reference).first()

        return None


class CheckoutView(CheckoutMixin, generic.FormView):
    template_name = 'forj/checkout/home.html'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['country'] = settings.DEFAULT_COUNTRY

        if self.request.method == 'POST':
            kwargs['diff'] = self.request.POST.get('diff')

        kwargs['order'] = self.order

        return kwargs

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            user.backend = settings.DEFAULT_AUTHENTICATION_BACKEND

            self.order = self.cart.save(user, order=self.order, defaults={
                'shipping_address': form.shipping_address,
                'billing_address': form.billing_address,
            })

        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return self.order.get_payment_url()


class OrderView(generic.DetailView):
    slug_field = 'reference'
    context_object_name = 'order'
    slug_url_kwarg = 'reference'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PaymentView(OrderView):
    template_name = 'forj/checkout/payment.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_status_succeeded():
            return redirect(self.object.get_payment_url())

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)


class SuccessView(OrderView):
    template_name = 'forj/checkout/success.html'

    def get_queryset(self):
        return super().get_queryset().filter(status=Order.STATUS_CHOICES.SUCCEEDED)


@csrf_exempt
def cart(request):
    params = getattr(request, request.method)

    action = params.get('action')

    cart = Cart.from_request(request)
    if cart is None:
        cart = Cart()

    reference = params.get('reference')

    if action is not None:
        if action == 'detail':
            if reference is None:
                return HttpResponseBadRequest('Missing `reference` parameter')

            try:
                product = Product.objects.from_reference(reference)
            except exceptions.InvalidProductRef as e:
                return HttpResponseBadRequest(e.message)

            return JsonResponse(product, encoder=JSONEncoder)
        elif action in ('add', 'remove'):
            if reference is None:
                return HttpResponseBadRequest('Missing `reference` parameter')

            try:
                if action == 'add':
                    cart.add_product(reference, params.get('quantity') or 1)
                elif action == 'remove':
                    cart.remove_product(reference)
            except exceptions.InvalidProductRef as e:
                return HttpResponseBadRequest(e.message)
        elif action == 'flush':
            cart = Cart.flush(request)

        cart.to_request(request)

    next_value = params.get('next')
    if next_value:
        try:
            return redirect(next_value)
        except NoReverseMatch:
            return HttpResponseBadRequest()

    return JsonResponse(cart.response, encoder=JSONEncoder)
