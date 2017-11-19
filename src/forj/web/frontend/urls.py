from django.conf.urls import url
from django.contrib.auth.decorators import login_required

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

    url(r'^checkout/(?P<reference>\w+)/success/$',
        login_required(views.SuccessView.as_view()),
        name='success'),

    url(r'^cart/$',
        views.cart,
        name='cart'),

    url(r'^collection/$',
        views.collection,
        name='collection'),
]
