from django.db import models
from django.utils.functional import cached_property

from forj.db.models import base
from forj.criteria import CriteriaSet
from forj.db.models.fields import AmountField
from forj import constants, exceptions


class ProductManager(base.Manager):
    def from_reference(self, reference):
        criteria_set = CriteriaSet.from_reference(reference)

        for product in self.all():
            if (criteria_set in product.criteria_set and
                    len(criteria_set) == len(product.criteria_set)):
                return product

        raise exceptions.InvalidProductRef('Product ref {} is not available'.format(reference))


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

    def __str__(self):
        return '{}: {}'.format(self.name, self.reference)

    @cached_property
    def criteria_set(self):
        return CriteriaSet.from_reference(self.reference)
