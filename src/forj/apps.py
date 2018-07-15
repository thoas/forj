import stripe

from django.apps import AppConfig
from django.conf import settings


class ForjConfig(AppConfig):
    name = "forj"
    verbose_name = "Forj"

    def ready(self):
        super(ForjConfig, self).ready()

        stripe.api_key = settings.STRIPE_SECRET_KEY
