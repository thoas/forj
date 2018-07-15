from django.conf.urls import url
from django.contrib import admin

from forj.urls import urlpatterns


urlpatterns = urlpatterns + [url(r"^", admin.site.urls)]
