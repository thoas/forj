from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.conf import settings
from django.contrib.auth import login
from django.db import transaction
from django.utils.functional import cached_property
from django.urls import NoReverseMatch
from django.views.generic.edit import FormMixin
from django.contrib import messages

from forj.web.frontend.forms import RegistrationForm, PaymentForm
from forj.models import Order, Product
from forj.cart import Cart
from forj import exceptions
from forj.encoders import JSONEncoder
from forj.payment.exceptions import CardError, PaymentError
from forj.payment import backend


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
        kwargs['order'] = self.order

        user = self.request.user
        if user.is_authenticated:
            kwargs['user'] = user

        return kwargs

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()

            self.order = self.cart.save(user, order=self.order, defaults={
                'shipping_address': form.shipping_address,
                'billing_address': form.billing_address,
            })

        if not self.request.user.is_authenticated:
            user.backend = settings.DEFAULT_AUTHENTICATION_BACKEND

            login(self.request, user)

            self.cart.to_request(self.request)

        return super().form_valid(form)

    def get_success_url(self):
        return self.order.get_payment_url()


class OrderView(generic.DetailView):
    slug_field = 'reference'
    context_object_name = 'order'
    slug_url_kwarg = 'reference'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PaymentProcessingView(OrderView):
    def get(self, request, *args, **kwargs):
        order = self.get_object()

        if order.is_status_succeeded():
            return redirect(order.get_success_url())

        try:
            order = backend.handle_order(order)
        except CardError:
            messages.error(self.request, _('Your card has been declined by your bank, we can\'t process the transaction'), fail_silently=True)

            return redirect(order.get_payment_url())
        except PaymentError:
            messages.error(self.request, _('An error occurred with our payment provider, we can\'t process the transaction'), fail_silently=True)

            return redirect(order.get_payment_url())

        if order.redirect_url:
            return redirect(order.redirect_url)

        if order.is_status_succeeded():
            return redirect(order.get_success_url())

        return order.get_payment_url()


class PaymentView(FormMixin, OrderView):
    template_name = 'forj/checkout/payment.html'
    form_class = PaymentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['order'] = self.object

        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_status_succeeded():
            return redirect(self.object.get_success_url())

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        try:
            order = form.save()
        except CardError:
            messages.error(self.request, _('Your card has been declined by your bank, we can\'t process the transaction'), fail_silently=True)

            return redirect(order.get_payment_url())
        except PaymentError:
            messages.error(self.request, _('An error occurred with our payment provider, we can\'t process the transaction'), fail_silently=True)

            return redirect(order.get_payment_url())

        if order.redirect_url:
            return redirect(order.redirect_url)

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_success_url()


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
