import shortuuid

from django.db import models

from forj import constants
from forj.db.models import base
from forj.db.models.fields import AmountField


class Order(base.Model):
    STATUS_CHOICES = constants.ORDER_STATUS_CHOICES
    SHIPPING_STATUS_CHOICES = constants.ORDER_SHIPPING_STATUS_CHOICES

    amount = AmountField(verbose_name='Total amount')
    currency = models.CharField(max_length=3,
                                choices=constants.CURRENCY_CHOICES,
                                default=constants.CURRENCY_CHOICES.EURO)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_CHOICES.WAITING)
    reference = models.CharField(max_length=30, verbose_name='Reference')
    shipping_status = models.PositiveSmallIntegerField(
        choices=SHIPPING_STATUS_CHOICES,
        default=SHIPPING_STATUS_CHOICES.WAITING)
    shipping_cost = AmountField(verbose_name='Shipping cost', default=0)
    user = models.ForeignKey('forj.User', on_delete=models.PROTECT)

    shipping_address = models.ForeignKey('forj.Address',
                                         on_delete=models.SET_NULL,
                                         related_name='shipping_orders',
                                         null=True)
    billing_address = models.ForeignKey('forj.Address',
                                        on_delete=models.SET_NULL,
                                        related_name='billing_orders',
                                        null=True)

    class Meta:
        abstract = False
        db_table = 'forj_order'

    def __str__(self):
        return '{}{}/{}'.format(self.get_currency_display(),
                                self.amount_converted,
                                self.get_status_display())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reference = shortuuid.uuid()

        super().save(*args, **kwargs)


class OrderItem(base.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Quantity', default=1)
    product = models.ForeignKey('forj.Product', related_name='items',
                                verbose_name='Product',
                                on_delete=models.CASCADE)
    shipping_cost = AmountField(verbose_name='Shipping cost', default=0)
    amount = AmountField(verbose_name='Total amount')
    product_reference = models.CharField(max_length=100,
                                         verbose_name='Product reference')

    class Meta:
        abstract = False
        db_table = 'forj_orderitem'
