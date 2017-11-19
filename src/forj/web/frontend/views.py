from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.conf import settings

from forj.web.frontend.forms import RegistrationForm


def home(request, template_name='forj/home.html'):
    return render(request, template_name)


def collection(request, template_name='forj/collection.html'):
    return render(request, template_name)


class CheckoutView(FormView):
    template_name = 'forj/checkout/home.html'
    form_class = RegistrationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['country'] = settings.DEFAULT_COUNTRY

        if self.request.method == 'POST':
            kwargs['diff'] = self.request.POST.get('diff')

        return kwargs

    def form_valid(self, form):
        user = form.save()

        return super().form_valid(form)


def payment(request, reference, template_name='forj/checkout/payment.html'):
    return render(request, template_name)


def cart(request):
    return HttpResponse('Ok')
