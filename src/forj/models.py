from django.db import models
from django.contrib.auth.models import AbstractUser


from forj.db.models import base
from forj.db.models.fields import AmountField


class Product(base.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    reference = models.CharField(max_length=50, verbose_name='Reference',
                                 db_index=True)
    description = models.TextField(null=True, verbose_name='Description')
    price = AmountField(verbose_name='Price')
    shipping_cost = AmountField(null=True, verbose_name='Shipping cost')

    class Meta:
        db_table = 'forj_product'
        abstract = False


class User(AbstractUser):
    class Meta:
        abstract = False
        swappable = 'AUTH_USER_MODEL'
        db_table = 'forj_user'


class Order(base.Model):
    amount = AmountField(verbose_name='Total amount')
    shipping_cost = AmountField(null=True, verbose_name='Shipping cost')
    user = models.ForeignKey('forj.User', on_delete=models.PROTECT)

    class Meta:
        abstract = False
        db_table = 'forj_order'
