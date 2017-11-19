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


class PaymentTest(TestCase):
    @fixture
    def path(self):
        return reverse('payment', args=[self.order.reference, ])

    def test_permission(self):
        response = self.client.get(self.path)

        assert response.status_code == 302

    def test_view(self):
        self.client.force_login(self.user)

        response = self.client.get(self.path)

        assert response.status_code == 200


class SuccessTest(TestCase):
    @fixture
    def path(self):
        return reverse('success', args=[self.order.reference, ])

    def test_permission(self):
        response = self.client.get(self.path)

        assert response.status_code == 302

    def test_view(self):
        self.client.force_login(self.user)

        response = self.client.get(self.path)

        assert response.status_code == 404

        self.order.mark_as_succeeded()

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
