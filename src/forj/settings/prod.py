import dotenv
import os

from .base import *  # noqa

dotenv.read_dotenv("/var/www/forj/.env")

DEBUG = False

STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

MEDIA_ROOT = "/var/www/forj/shared/media"
STATIC_ROOT = "/var/www/forj/shared/static"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

PARENT_HOST = "forj.shop"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "in.mailjet.com"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
SERVER_EMAIL = "noreply@forj.shop"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
