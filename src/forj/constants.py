from extended_choices import Choices

from django.utils.translation import gettext_lazy as _

ORDER_STATUS_CHOICES = Choices(
    ("WAITING", 1, "Waiting"), ("SUCCEEDED", 2, "Succeeded"), ("FAILED", 3, "Failed")
)

CURRENCY_CHOICES = Choices(("EURO", "EUR", "€"))

ORDER_SHIPPING_STATUS_CHOICES = Choices(
    ("WAITING", 1, "Waiting"),
    ("PROCESSING", 2, "Processing"),
    ("DELIVERED", 3, "Delivered"),
)

ADDRESS_TYPE_CHOICES = Choices(
    ("INDIVIDUAL", 1, _("Individual")), ("BUSINESS", 2, _("Business"))
)
