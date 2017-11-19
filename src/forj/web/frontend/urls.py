from django.conf.urls import url

from . import views

from forj.urls import urlpatterns


urlpatterns = urlpatterns + [
    url(r'^$', views.home, name='home'),
    url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/(?P<reference>\w+)/payment/$', views.payment, name='payment'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^collection/$', views.collection, name='collection'),
]
