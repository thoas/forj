from forj.utils.test import TestCase
from forj.cart import Cart


class CartTest(TestCase):
    def test_add_product(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 2)

        assert self.cart.amount == self.p3_empty.price * 2

        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)

        assert self.cart.amount == self.p3_empty.price * 3

        self.cart.add_product("LA(25)-LO(25)-P(AGLO)-H(40)", 1)

        assert self.cart.amount == self.p3_empty.price * 3 + self.p1_aglo.price

    def test_remove_product(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 2)

        assert self.cart.amount == self.p3_empty.price * 2

        self.cart.remove_product("LA(37)-LO(122)-H(67)")

        assert self.cart.amount == 0

        self.cart.add_product("LA(25)-LO(25)-P(AGLO)-H(40)", 1)

        assert self.cart.amount == self.p1_aglo.price

    def test_serialized_data(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 2)
        self.cart.add_product("LA(37)-LO(50)-H(50)", 4)

        self.cart.serialized_data == '{"LA(37)-LO(122)-H(67)": 2, "LA(37)-LO(50)-H(50)": 4}'

        self.cart.remove_product("LA(37)-LO(50)-H(50)")

        self.cart.serialized_data == '{"LA(37)-LO(122)-H(67)": 2}'

    def test_to_request(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)
        self.cart.add_product("LA(37)-LO(50)-H(50)", 1)

        request = self.factory.get("/")
        request.session = self.session_store

        cart = Cart.from_request(request)
        assert cart is None

        self.cart.to_request(request)

        cart = Cart.from_request(request)
        assert (
            cart.serialized_data
            == '{"LA(37)-LO(122)-H(67)": 1, "LA(37)-LO(50)-H(50)": 1}'
        )

    def test_save(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)
        self.cart.add_product("LA(37)-LO(50)-H(50)", 1)

        order = self.cart.save()

        assert order.items.count() == 2

        items = order.items.all()

        assert sum([item.quantity for item in items]) == 2

        references = (
            "LA(37)-LO(50)-H(50)",
            "LA(37)-LO(122)-H(67)"
        )

        items = dict((item.product_reference, item) for item in items)

        for reference in references:
            assert reference in items
            assert items[reference].quantity == 1
