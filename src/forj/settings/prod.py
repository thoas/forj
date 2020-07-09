import dotenv
import os

from .base import *  # noqa

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

dotenv.read_dotenv("/var/www/forj/.env")

DEBUG = False

STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

MEDIA_ROOT = "/var/www/forj/shared/media"
STATIC_ROOT = "/var/www/forj/shared/static"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

PARENT_HOST = "table-forj.fr"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "in.mailjet.com"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
SERVER_EMAIL = "noreply@forj.shop"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SESSION_COOKIE_DOMAIN = ".table-forj.fr"
CSRF_COOKIE_DOMAIN = ".table-forj.fr"

sentry_dsn = os.getenv("SENTRY_DSN")

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
