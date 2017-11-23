from django.conf import settings

from forj import constants


def base(request):
    default_currency = settings.DEFAULT_CURRENCY

    _, _, value = constants.CURRENCY_CHOICES.values[default_currency]

    return {
        'CURRENCY': default_currency,
        'CURRENCY_DISPLAY': value
    }
