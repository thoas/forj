from forj.utils.test import TestCase
from forj.models import Product, Order


class ProductTest(TestCase):
    def test_from_reference(self):
        p = Product.objects.from_reference('LA(37)-LO(122)-H(67)')
        p == self.p3_empty

        p = Product.objects.from_reference('LA(25)-LO(25)-P(AGLO)-H(40)')
        p == self.p1_aglo

        p = Product.objects.from_reference('LA(26)-LO(101)-P(AGLO)-H(40)')
        p == self.p1_aglo

        p = Product.objects.from_reference('LA(112)-LO(33)-P(ACIER)-H(67)')
        p == self.p2_acier


class OrderTest(TestCase):
    def test_to_request(self):
        request = self.factory.get('/')
        request.session = self.session_store

        self.order.to_request(request)

        order = Order.objects.from_request(request)

        assert order is not None
