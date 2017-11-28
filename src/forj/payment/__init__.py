from django.utils.module_loading import import_string
from django.conf import settings


backend = import_string(settings.FORJ_PAYMENT_BACKEND_CLASS)()
