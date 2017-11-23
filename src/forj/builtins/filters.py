from django.template.defaultfilters import floatformat
from django.conf import settings


def amountformat(value, precision=settings.AMOUNT_PRECISION):
    return floatformat(value / 100.0, precision)
