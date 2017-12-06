from django.conf import settings

from forj import constants


def base(request):
    default_currency = settings.DEFAULT_CURRENCY

    _, _, value = constants.CURRENCY_CHOICES.values[default_currency]

    return {
        'STATIC_URL': settings.STATIC_URL,
        'CURRENCY': default_currency,
        'CURRENCY_DISPLAY': value,
        'AMOUNT_PRECISION': settings.AMOUNT_PRECISION,
        'STRIPE_PUBLISHABLE_KEY': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None),
        'STRIPE_SECRET_KEY': getattr(settings, 'STRIPE_SECRET_KEY', None),
    }
