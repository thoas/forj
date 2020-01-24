import importlib

from functools import lru_cache

from django import test
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from exam import Exam, fixture, before

from forj.models import Product, User, Address
from forj.cart import Cart


@lru_cache()
def get_session_store():
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.file"
    engine = importlib.import_module("django.contrib.sessions.backends.file")
    store = engine.SessionStore()
    store.save()

    return store


class TestCase(Exam, test.TestCase):
    @fixture
    def anonymous(self):
        return AnonymousUser()

    @fixture
    def cart(self):
        return Cart()

    @fixture
    def user(self):
        return User.objects.create_user("newbie@example.com", "$ecret")

    @fixture
    def session_store(self):
        return get_session_store()

    @fixture
    def factory(self):
        return RequestFactory()

    @before
    def init_products(self):
        self.p1_aglo = Product.objects.create(
            name="AGLO<=1m2",
            reference="LA(25/100)-LO(25/100)-P(AGLO)-H(40/120)",
            price=47000 * 1.5,
        )

        self.p2_aglo = Product.objects.create(
            name="AGLO<=1m2",
            reference="LA(100/120)-LO(25/83)-P(AGLO)-H(40/120)",
            price=47000 * 1.5,
        )

        self.p3_aglo = Product.objects.create(
            name="AGLO<=1m2",
            reference="LA(25/50)-LO(100/200)-P(AGLO)-H(40/120)",
            price=47000 * 1.5,
        )

        self.p4_aglo = Product.objects.create(
            name="AGLO>1m2",
            reference="LA(101/120)-LO(101/220)-P(AGLO)-H(40/120)-R(?)",
            formula="(LA/100*LO/100*120+LA/100*LO/100*40+LA/100*LO/100*40+42+LA/100*LO/100*60)*1.5",
        )

        self.p1_acier = Product.objects.create(
            name="ACIER<=1m2",
            reference="LA(25/100)-LO(25/100)-P(ACIER)-H(40/120)",
            price=47000 * 1.5,
        )

        self.p2_acier = Product.objects.create(
            name="ACIER<=1m2",
            reference="LA(100/120)-LO(25/83)-P(ACIER)-H(40/120)",
            price=47000 * 1.5,
        )

        self.p3_acier = Product.objects.create(
            name="ACIER<=1m2",
            reference="LA(25/50)-LO(100/200)-P(ACIER)-H(40/120)",
            price=47000 * 1.5,
        )

        self.p1_brut = Product.objects.create(
            name="BRUT<=1m2",
            reference="LA(25/100)-LO(25/100)-P(BRUT)-H(40/120)",
            price=60100 * 1.5,
        )

        self.p2_brut = Product.objects.create(
            name="BRUT<=1m2",
            reference="LA(100/120)-LO(25/83)-P(BRUT)-H(40/120)",
            price=60100 * 1.5,
        )

        self.p3_brut = Product.objects.create(
            name="BRUT<=1m2",
            reference="LA(25/50)-LO(100/200)-P(BRUT)-H(40/120)",
            price=60100 * 1.5,
        )

        self.p1_acierext = Product.objects.create(
            name="ACIEREXT<=1m2",
            reference="LA(25/100)-LO(25/100)-P(ACIEREXT)-H(40/120)",
            price=83000 * 1.5,
        )

        self.p2_acierext = Product.objects.create(
            name="ACIEREXT<=1m2",
            reference="LA(100/120)-LO(25/83)-P(ACIEREXT)-H(40/120)",
            price=83000 * 1.5,
        )

        self.p3_acierext = Product.objects.create(
            name="ACIEREXT<=1m2",
            reference="LA(25/50)-LO(100/200)-P(ACIEREXT)-H(40/120)",
            price=83000 * 1.5,
        )

        self.p1_empty = Product.objects.create(
            name="SANS PLATEAU<=1m2",
            reference="LA(25/100)-LO(25/100)-H(40/120)",
            price=36200 * 1.5,
        )

        self.p2_empty = Product.objects.create(
            name="SANS PLATEAU<=1m2",
            reference="LA(100/120)-LO(25/83)-H(40/120)",
            price=36200 * 1.5,
        )

        self.p3_empty = Product.objects.create(
            name="SANS PLATEAU<=1m2",
            reference="LA(25/50)-LO(100/200)-H(40/120)",
            price=36200 * 1.5,
        )

    @fixture
    def order(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)
        self.cart.add_product("LA(37)-LO(50)-H(50)", 1)

        order = self.cart.save()
        order.shipping_address = Address.objects.create(email="florent@forj.shop")
        order.save(update_fields=("shipping_address",))

        return order
