from forj.utils.test import TestCase

from django.urls import reverse


class ViewsTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))

        assert response.status_code == 200

    def test_checkout_view(self):
        response = self.client.get(reverse('checkout'))

        assert response.status_code == 200

    def test_cart_view(self):
        response = self.client.get(reverse('cart'))

        assert response.status_code == 200
