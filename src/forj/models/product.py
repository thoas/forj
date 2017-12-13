from django.db import models
from django.utils.functional import cached_property
from django.conf import settings

from forj.db.models import base
from forj.criteria import CriteriaSet
from forj.db.models.fields import AmountField
from forj import constants, exceptions
from forj.utils.math import expr


class ProductManager(base.Manager):
    def from_reference(self, reference):
        criteria_set = CriteriaSet.from_reference(reference)

        for product in self.order_by('price'):
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
                                default=settings.DEFAULT_CURRENCY)
    shipping_cost = AmountField(null=True, verbose_name='Shipping cost',
                                default=0)

    tax_cost = AmountField(null=True, verbose_name='Tax cost',
                           default=0)

    objects = ProductManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        db_table = 'forj_product'
        abstract = False

    def __str__(self):
        return '{}: {}'.format(self.name, self.reference)

    def get_price(self, reference):
        if not self.formula:
            return self.price

        formula = self.formula

        for criteria in CriteriaSet.from_reference(reference):
            formula = formula.replace(criteria.name, criteria.value)

        return round(expr(formula), 2)

    @cached_property
    def criteria_set(self):
        return CriteriaSet.from_reference(self.reference)

    @property
    def serialized_data(self):
        return {
            'id': self.pk,
            'price': self.price,
            'shipping_cost': self.shipping_cost,
            'description': self.description,
            'name': self.name,
            'currency': self.currency
        }
