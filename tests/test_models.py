from forj.utils.test import TestCase
from forj.models import Product


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
