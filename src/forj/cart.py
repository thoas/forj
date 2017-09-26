from django.db import transaction

from forj.models import Product, Order, OrderItem


class Cart(object):
    def __init__(self):
        self.products = []
        self.amount = 0
        self.shipping_cost = 0

    def add_product(self, product):
        pass

    @classmethod
    def from_request(cls, request):
        pass

    def to_request(self, request):
        pass

    @transaction.atomic
    def save(self):
        pass
