from django.shortcuts import render
from django.http import HttpResponse


def home(request, template_name='home.html'):
    return render(request, template_name)


def collection(request, template_name='collection.html'):
    return render(request, template_name)


def checkout(request, template_name='checkout.html'):
    return render(request, template_name)


def cart(request):
    return HttpResponse('Ok')
