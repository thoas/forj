from forj.utils.test import TestCase

from django.urls import reverse

from exam import fixture


class HomeTest(TestCase):
    @fixture
    def path(self):
        return reverse('home')

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200


class CheckoutTest(TestCase):
    @fixture
    def path(self):
        return reverse('checkout')

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200


class CartTest(TestCase):
    @fixture
    def path(self):
        return reverse('cart')

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200


class CollectionTest(TestCase):
    @fixture
    def path(self):
        return reverse('collection')

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200
