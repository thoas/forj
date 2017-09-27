import simplejson as json

from django.db import transaction

from collections import defaultdict

from forj.models import Product, Order, OrderItem

CART_SESSION_KEY = 'cart_id'


class Cart(object):
    def __init__(self):
        self.products = {}
        self.amount = 0
        self.shipping_cost = 0

    def add_product(self, reference, quantity=1):
        product = Product.objects.from_reference(reference)

        if product.pk not in self.products:
            self.products[product.pk] = {
                'obj': product,
                'references': defaultdict(int),
            }

        self.products[product.pk]['references'][reference] += quantity

        self.update()

    def remove_product(self, reference):
        product = Product.objects.from_reference(reference)

        if product.pk in self.products:
            del self.products[product.pk]

        self.update()

    def update(self):
        self.amount = 0
        self.shipping_cost = 0

        for product_id, result in self.products.items():
            quantity = sum(result['references'].values())

            self.amount += quantity * result['obj'].price
            self.shipping_cost += quantity * result['obj'].shipping_cost

    @property
    def data(self):
        data = {}
        for product_id, result in self.products.items():
            data.update(result['references'])

        return data

    @property
    def serialized_data(self):
        return json.dumps(self.data)

    @classmethod
    def from_serialized_data(cls, data):
        return cls.from_data(json.loads(data))

    @classmethod
    def from_data(cls, data):
        return cls()

    @classmethod
    def from_request(cls, request):
        return cls.from_serialized_data(request.session.get(CART_SESSION_KEY))

    def to_request(self, request):
        request.session.set(CART_SESSION_KEY, self.serialized_data)

    @transaction.atomic
    def save(self):
        pass
