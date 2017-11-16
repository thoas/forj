from django.shortcuts import render
from django.http import HttpResponse

from forj.web.frontend.forms import RegistrationForm


def home(request, template_name='forj/home.html'):
    return render(request, template_name)


def collection(request, template_name='forj/collection.html'):
    return render(request, template_name)


def checkout(request, template_name='forj/checkout/home.html'):
    form = RegistrationForm()

    return render(request, template_name, {
        'form': form
    })


def payment(request, reference, template_name='forj/checkout/payment.html'):
    return render(request, template_name)


def cart(request):
    return HttpResponse('Ok')
