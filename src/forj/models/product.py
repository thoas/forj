from django.db import models
from django.utils.functional import cached_property
from django.conf import settings

from forj.db.models import base
from forj.criteria import CriteriaSet
from forj.db.models.fields import AmountField
from forj import constants, exceptions
from forj.utils.math import expr


class ProductQuerySet(base.QuerySet):
    def from_reference(self, reference):
        for product in self:
            if product.handle_reference(reference):
                return product

        raise exceptions.InvalidProductRef('Product ref {} is not available'.format(reference))


class ProductManager(base.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)

    def from_reference(self, reference):
        return self.order_by('price', '-condition').from_reference(reference)


class Product(base.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    reference = models.CharField(max_length=100, verbose_name='Reference',
                                 db_index=True)
    description = models.TextField(null=True, verbose_name='Description',
                                   blank=True)
    price = AmountField(verbose_name='Price', null=True, blank=True)
    formula = models.CharField(max_length=100, verbose_name='Formula',
                               null=True, blank=True)
    condition = models.CharField(max_length=100, verbose_name='Condition',
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

    def handle_reference(self, reference):
        criteria_set = CriteriaSet.from_reference(reference)

        if (criteria_set in self.criteria_set and
                len(criteria_set) == len(self.criteria_set)):

            if not self.condition:
                return True

            cond = self.condition

            for criteria in criteria_set:
                cond = cond.replace(criteria.name, criteria.value)

            if expr(cond):
                return True

        return False

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

    def format_description(self, reference):
        if not self.description:
            return None

        description = self.description

        for criteria in CriteriaSet.from_reference(reference):
            description = description.replace('{%s}' % criteria.name, criteria.value)

        return description

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
