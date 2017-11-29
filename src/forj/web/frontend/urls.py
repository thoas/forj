from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views import generic

from . import views

from forj.urls import urlpatterns


urlpatterns = urlpatterns + [
    url(r'^$',
        views.home,
        name='home'),

    url(r'^checkout/(?:(?P<reference>\w+)/)?$',
        views.CheckoutView.as_view(),
        name='checkout'),

    url(r'^checkout/(?P<reference>\w+)/payment/$',
        login_required(views.PaymentView.as_view()),
        name='payment'),

    url(r'^checkout/(?P<reference>\w+)/payment/processing/$',
        login_required(views.PaymentProcessingView.as_view()),
        name='payment_processing'),

    url(r'^checkout/(?P<reference>\w+)/success/$',
        login_required(views.SuccessView.as_view()),
        name='success'),

    url(r'^checkout/(?P<reference>\w+)/invoice/$',
        login_required(views.InvoiceView.as_view()),
        name='invoice'),

    url(r'^cart/$',
        views.cart,
        name='cart'),

    url(r'^handler404/',
        generic.TemplateView.as_view(template_name='404.html')),

    url(r'^handler500/',
        generic.TemplateView.as_view(template_name='500.html')),

    url(r'^collection/$',
        views.collection,
        name='collection'),
]
