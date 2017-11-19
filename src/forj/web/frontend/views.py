from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.conf import settings
from django.contrib.auth import login
from django.urls import reverse

from forj.web.frontend.forms import RegistrationForm
from forj.models import Order


def home(request, template_name='forj/home.html'):
    return render(request, template_name)


def collection(request, template_name='forj/collection.html'):
    return render(request, template_name)


class CheckoutView(generic.FormView):
    template_name = 'forj/checkout/home.html'
    form_class = RegistrationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['country'] = settings.DEFAULT_COUNTRY

        if self.request.method == 'POST':
            kwargs['diff'] = self.request.POST.get('diff')

        if self.request.user.is_authenticated:
            reference = self.kwargs.get('reference')

            if reference:
                kwargs['order'] = Order.objects.filter(user=self.request.user,
                                                       reference=reference).first()

        return kwargs

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user.backend = settings.DEFAULT_AUTHENTICATION_BACKEND

        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('payment', args=['foo'])


class OrderView(generic.DetailView):
    slug_field = 'reference'
    context_object_name = 'order'
    slug_url_kwarg = 'reference'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PaymentView(OrderView):
    template_name = 'forj/checkout/payment.html'


class SuccessView(OrderView):
    template_name = 'forj/checkout/success.html'

    def get_queryset(self):
        return super().get_queryset().filter(status=Order.STATUS_CHOICES.SUCCEEDED)


def cart(request):
    return HttpResponse('Ok')
