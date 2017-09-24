from forj.utils.test import TestCase
from forj.models import Product

from exam import before


class ProductTest(TestCase):
    @before
    def init_products(self):
        self.p1 = Product.objects.create(
            name='AGLO<=1m2',
            reference='LA(25/100)-LO(25/100)-P(AGLO)-H(40/120)'
        )

        self.p2 = Product.objects.create(
            name='ACIER<=1m2',
            reference='LA(25/100)-LO(25/100)-P(ACIER)-H(40/120)'
        )

        self.p3 = Product.objects.create(
            name='BRUT<=1m2',
            reference='LA(25/100)-LO(25/100)-P(BRUT)-H(40/120)'
        )

        self.p4 = Product.objects.create(
            name='BRUT<=1m2',
            reference='LA(25/100)-LO(25/100)-P(BRUT)-H(40/120)'
        )

        self.p5 = Product.objects.create(
            name='ACIEREXT<=1m2',
            reference='LA(25/100)-LO(25/100)-P(ACIEREXT)-H(40/120)'
        )

        self.p6 = Product.objects.create(
            name='SANS PLATEAU<=1m2',
            reference='LA(25/100)-LO(25/100)-H(40/120)'
        )

    def test_from_reference(self):
        p = Product.objects.from_reference('LA(25)-LO(25)-P(AGLO)-H(40)')
        p == self.p1
