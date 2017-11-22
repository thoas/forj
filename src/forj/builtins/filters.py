from django.template.defaultfilters import floatformat


def amountformat(value, precision):
    return floatformat(value / 100.0, precision)
