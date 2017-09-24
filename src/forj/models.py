from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.functional import cached_property

from django_countries.fields import CountryField

from forj.db.models import base
from forj.db.models.fields import AmountField
from forj import constants
from forj.criteria import CriteriaSet


class ProductManager(base.Manager):
    def from_reference(self, reference):
        criteria_set = CriteriaSet.from_reference(reference)

        for product in self.all():
            if (criteria_set in product.criteria_set and
                    len(criteria_set) == len(product.criteria_set)):
                return product

        return None


class Product(base.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    reference = models.CharField(max_length=100, verbose_name='Reference',
                                 db_index=True)
    description = models.TextField(null=True, verbose_name='Description',
                                   blank=True)
    price = AmountField(verbose_name='Price', null=True, blank=True)
    formula = models.CharField(max_length=100, verbose_name='Formula',
                               null=True, blank=True)
    currency = models.CharField(max_length=3,
                                choices=constants.CURRENCY_CHOICES,
                                default=constants.CURRENCY_CHOICES.EURO)
    shipping_cost = AmountField(null=True, verbose_name='Shipping cost',
                                default=0)

    objects = ProductManager()

    class Meta:
        db_table = 'forj_product'
        abstract = False

    @cached_property
    def criteria_set(self):
        return CriteriaSet.from_reference(self.reference)


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
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_CHOICES.WAITING)
    shipping_status = models.PositiveSmallIntegerField(
        choices=SHIPPING_STATUS_CHOICES,
        default=SHIPPING_STATUS_CHOICES.WAITING)
    shipping_cost = AmountField(verbose_name='Shipping cost', default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

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


class Address(base.Model):
    TYPE_CHOICES = constants.ADDRESS_TYPE_CHOICES

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES,
                                            default=TYPE_CHOICES.INDIVIDUAL,
                                            null=True)

    first_name = models.CharField(max_length=250, verbose_name='First name',
                                  null=True,
                                  blank=True)
    last_name = models.CharField(max_length=250,
                                 verbose_name='Last name',
                                 null=True, blank=True)
    business_name = models.CharField(max_length=250,
                                     verbose_name='Entity name',
                                     null=True, blank=True)
    line1 = models.TextField(verbose_name='Address', null=True)
    line2 = models.TextField(verbose_name='Address 2', null=True, blank=True)
    postal_code = models.CharField(max_length=140,
                                   verbose_name='Postal code',
                                   null=True)
    city = models.CharField(max_length=140,
                            verbose_name='City',
                            null=True)
    country = CountryField(blank=True, null=True,
                           verbose_name='Country',
                           default=settings.DEFAULT_COUNTRY)

    user = models.ForeignKey(User, related_name='addresses',
                             on_delete=models.PROTECT)

    class Meta:
        abstract = False
        db_table = 'forj_address'
