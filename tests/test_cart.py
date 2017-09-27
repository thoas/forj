from forj.utils.test import TestCase
from forj.cart import Cart

from exam import fixture


class CartTest(TestCase):
    @fixture
    def cart(self):
        return Cart()

    def test_to_request(self):
        pass

    def test_add_product(self):
        self.cart.add_product('LA(37)-LO(122)-H(67)', 2)

        assert self.cart.amount == self.p3_empty.price * 2

        self.cart.add_product('LA(37)-LO(122)-H(67)', 1)

        assert self.cart.amount == self.p3_empty.price * 3

        self.cart.add_product('LA(25)-LO(25)-P(AGLO)-H(40)', 1)

        assert self.cart.amount == self.p3_empty.price * 3 + self.p1_aglo.price

    def test_remove_product(self):
        self.cart.add_product('LA(37)-LO(122)-H(67)', 2)

        assert self.cart.amount == self.p3_empty.price * 2

        self.cart.remove_product('LA(37)-LO(122)-H(67)')

        assert self.cart.amount == 0

        self.cart.add_product('LA(25)-LO(25)-P(AGLO)-H(40)', 1)

        assert self.cart.amount == self.p1_aglo.price
