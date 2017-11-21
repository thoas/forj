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
                'refs': defaultdict(int),
            }

        self.products[product.pk]['refs'][reference] += quantity

        self.update()

    def remove_product(self, reference):
        product = Product.objects.from_reference(reference)

        if product.pk in self.products:
            del self.products[product.pk]

        self.update()

    def update(self):
        self.amount = 0
        self.shipping_cost = 0
        self.total = 0

        for product_id, result in self.products.items():
            quantity = sum(result['refs'].values())

            self.amount += quantity * result['obj'].price
            self.shipping_cost += quantity * result['obj'].shipping_cost
            self.total += self.amount + self.shipping_cost

    @property
    def data(self):
        data = {}
        for product_id, result in self.products.items():
            data.update(result['refs'])

        return data

    @property
    def serialized_data(self):
        return json.dumps(self.data)

    @classmethod
    def from_serialized_data(cls, data):
        return cls.from_data(json.loads(data))

    @classmethod
    def from_data(cls, data):
        cart = cls()

        for reference, quantity in data.items():
            cart.add_product(reference, quantity)

        return cart

    @classmethod
    def from_request(cls, request):
        result = request.session.get(CART_SESSION_KEY)
        if result is None:
            return None

        return cls.from_serialized_data(result)

    def to_request(self, request):
        session = request.session
        session[CART_SESSION_KEY] = self.serialized_data
        session.save()

    @transaction.atomic
    def save(self, user, commit=True, order=None, defaults=None):
        defaults = defaults or {}

        self.update()

        if order is None:
            order = Order(user=user)

        order.amount = self.amount
        order.shipping_cost = self.shipping_cost

        for k, v in defaults.items():
            setattr(order, k, v)

        order_items = []

        for product_id, result in self.products.items():
            product = result['obj']

            for ref, quantity in result['refs'].items():
                shipping_cost = quantity * product.shipping_cost

                order_item = OrderItem(order=order,
                                       quantity=quantity,
                                       amount=quantity * product.price,
                                       product_reference=ref,
                                       shipping_cost=shipping_cost,
                                       product=product)
                order_items.append(order_item)

        if commit is True:
            if order.pk:
                order.items.all().delete()

            order.save()

            for order_item in order_items:
                order_item.order = order

            OrderItem.objects.bulk_create(order_items)

        return order
