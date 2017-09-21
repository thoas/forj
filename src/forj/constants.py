from extended_choices import Choices


ORDER_STATUS_CHOICES = Choices(
    ('WAITING', 1, 'Waiting'),
    ('SUCCEEDED', 2, 'Succeeded'),
    ('FAILED', 3, 'Failed'),
)

CURRENCY_CHOICES = Choices(
    ('EURO', 'EUR', '€')
)

ORDER_SHIPPING_STATUS_CHOICES = Choices(
    ('WAITING', 1, 'Waiting'),
    ('PROCESSING', 2, 'Processing'),
    ('DELIVERED', 3, 'Delivered'),
)
