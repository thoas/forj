from .base import *  # noqa

INSTALLED_APPS += ("debug_toolbar",)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]


try:
    from .credentials import *
except ImportError:
    pass
