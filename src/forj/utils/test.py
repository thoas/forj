import importlib

from django import test
from django.utils.lru_cache import lru_cache
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from exam import Exam, fixture, before

from forj.models import Product


@lru_cache()
def get_session_store():
    settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
    engine = importlib.import_module('django.contrib.sessions.backends.file')
    store = engine.SessionStore()
    store.save()

    return store


class TestCase(Exam, test.TestCase):
    @fixture
    def anonymous(self):
        return AnonymousUser()

    @fixture
    def session_store(self):
        return get_session_store()

    @fixture
    def factory(self):
        return RequestFactory()

    @before
    def init_products(self):
        self.p1_aglo = Product.objects.create(
            name='AGLO<=1m2',
            reference='LA(25/100)-LO(25/100)-P(AGLO)-H(40/120)',
            price=47000 * 1.5,
        )

        self.p2_aglo = Product.objects.create(
            name='AGLO<=1m2',
            reference='LA(100/120)-LO(25/83)-P(AGLO)-H(40/120)',
            price=47000 * 1.5,
        )

        self.p3_aglo = Product.objects.create(
            name='AGLO<=1m2',
            reference='LA(25/50)-LO(100/200)-P(AGLO)-H(40/120)',
            price=47000 * 1.5,
        )

        self.p1_acier = Product.objects.create(
            name='ACIER<=1m2',
            reference='LA(25/100)-LO(25/100)-P(ACIER)-H(40/120)',
            price=47000 * 1.5,
        )

        self.p2_acier = Product.objects.create(
            name='ACIER<=1m2',
            reference='LA(100/120)-LO(25/83)-P(ACIER)-H(40/120)',
            price=47000 * 1.5,
        )

        self.p3_acier = Product.objects.create(
            name='ACIER<=1m2',
            reference='LA(25/50)-LO(100/200)-P(ACIER)-H(40/120)',
            price=47000 * 1.5,
        )

        self.p1_brut = Product.objects.create(
            name='BRUT<=1m2',
            reference='LA(25/100)-LO(25/100)-P(BRUT)-H(40/120)',
            price=60100 * 1.5,
        )

        self.p2_brut = Product.objects.create(
            name='BRUT<=1m2',
            reference='LA(100/120)-LO(25/83)-P(BRUT)-H(40/120)',
            price=60100 * 1.5,
        )

        self.p3_brut = Product.objects.create(
            name='BRUT<=1m2',
            reference='LA(25/50)-LO(100/200)-P(BRUT)-H(40/120)',
            price=60100 * 1.5,
        )

        self.p1_acierext = Product.objects.create(
            name='ACIEREXT<=1m2',
            reference='LA(25/100)-LO(25/100)-P(ACIEREXT)-H(40/120)',
            price=83000 * 1.5,
        )

        self.p2_acierext = Product.objects.create(
            name='ACIEREXT<=1m2',
            reference='LA(100/120)-LO(25/83)-P(ACIEREXT)-H(40/120)',
            price=83000 * 1.5,
        )

        self.p3_acierext = Product.objects.create(
            name='ACIEREXT<=1m2',
            reference='LA(25/50)-LO(100/200)-P(ACIEREXT)-H(40/120)',
            price=83000 * 1.5,
        )

        self.p1_empty = Product.objects.create(
            name='SANS PLATEAU<=1m2',
            reference='LA(25/100)-LO(25/100)-H(40/120)',
            price=36200 * 1.5
        )

        self.p2_empty = Product.objects.create(
            name='SANS PLATEAU<=1m2',
            reference='LA(100/120)-LO(25/83)-H(40/120)',
            price=36200 * 1.5
        )

        self.p3_empty = Product.objects.create(
            name='SANS PLATEAU<=1m2',
            reference='LA(25/50)-LO(100/200)-H(40/120)',
            price=36200 * 1.5
        )
