from forj.utils.test import TestCase
from forj.models import Product, Order


class ProductTest(TestCase):
    def test_from_reference(self):
        p = Product.objects.from_reference("TABLE-DESIGN")
        assert p == self.p4_fixed

        p = Product.objects.from_reference("TABOURET-DESIGN")
        assert p == self.p5_fixed

        p = Product.objects.from_reference("LA(37)-LO(122)-H(67)")
        assert p == self.p3_empty

        p = Product.objects.from_reference("LA(25)-LO(25)-P(AGLO)-H(40)")
        assert p == self.p1_aglo

        p = Product.objects.from_reference("LA(26)-LO(101)-P(AGLO)-H(40)")
        assert p == self.p3_aglo

        p = Product.objects.from_reference("LA(112)-LO(33)-P(ACIER)-H(67)")
        assert p == self.p2_acier

    def test_get_price(self):
        price = self.p4_aglo.get_price("LA(106)-LO(124)-P(AGLO)-H(61)-R(NOIR)")

        assert price == 575.62


class OrderTest(TestCase):
    def test_to_request(self):
        request = self.factory.get("/")
        request.session = self.session_store

        self.order.to_request(request)

        order = Order.objects.from_request(request)

        assert order is not None
