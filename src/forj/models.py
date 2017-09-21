from django.db import models
from django.contrib.auth.models import AbstractUser

from forj.db.models import base
from forj.db.models.fields import AmountField
from forj import constants


class Product(base.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    reference = models.CharField(max_length=50, verbose_name='Reference',
                                 db_index=True)
    description = models.TextField(null=True, verbose_name='Description',
                                   blank=True)
    price = AmountField(verbose_name='Price')
    currency = models.CharField(max_length=3,
                                choices=constants.CURRENCY_CHOICES,
                                default=constants.CURRENCY_CHOICES.EURO)
    shipping_cost = AmountField(null=True, verbose_name='Shipping cost',
                                default=0)

    class Meta:
        db_table = 'forj_product'
        abstract = False


class User(AbstractUser):
    class Meta:
        abstract = False
        swappable = 'AUTH_USER_MODEL'
        db_table = 'forj_user'


class Order(base.Model):
    STATUS_CHOICES = constants.ORDER_STATUS_CHOICES
    SHIPPING_STATUS_CHOICES = constants.ORDER_SHIPPING_STATUS_CHOICES

    amount = AmountField(verbose_name='Total amount')
    currency = models.CharField(max_length=3,
                                choices=constants.CURRENCY_CHOICES,
                                default=constants.CURRENCY_CHOICES.EURO)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,
                                      default=STATUS_CHOICES.WAITING)
    shipping_status = models.SmallIntegerField(choices=SHIPPING_STATUS_CHOICES,
                                               default=SHIPPING_STATUS_CHOICES.WAITING)
    shipping_cost = AmountField(verbose_name='Shipping cost', default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        abstract = False
        db_table = 'forj_order'


class OrderItem(base.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Quantity', default=1)
    product = models.ForeignKey(Product, related_name='items',
                                verbose_name='Product',
                                on_delete=models.CASCADE)

    class Meta:
        abstract = False
        db_table = 'forj_orderitem'
