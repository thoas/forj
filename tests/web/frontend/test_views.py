from forj.utils.test import TestCase
from forj import constants
from forj.models import User

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

    def test_complete(self):
        self.cart.add_product('LA(37)-LO(122)-H(67)', 1)
        self.cart.add_product('LA(37)-LO(50)-H(50)', 1)

        self.cart.to_request(self.client)

        response = self.client.get(self.path)

        assert response.status_code == 200

        data = {
            'shipping-address-type': constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            'shipping-address-first_name': 'Florent',
            'shipping-address-last_name': 'Messa',
            'shipping-address-city': 'Paris',
            'shipping-address-phone_number': '0183629075',
            'shipping-address-line1': '8 rue saint fiacre',
            'shipping-address-postal_code': '75002',
            'user-email': 'flo@ulule.com',
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302

        user = User.objects.filter(email='flo@ulule.com').first()
        assert user is not None
        assert user.orders.count() == 1

        order = user.orders.first()
        assert order.items.count() == 2
        assert response['Location'] == order.get_payment_url()
        assert order.shipping_address_id is not None


class CheckoutUpdateTest(TestCase):
    @fixture
    def order(self):
        self.cart.add_product('LA(37)-LO(122)-H(67)', 1)
        self.cart.add_product('LA(37)-LO(50)-H(50)', 1)

        return self.cart.save(self.user)

    @property
    def path(self):
        return self.order.get_checkout_url()

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200

    def test_update(self):
        self.cart.to_request(self.client)

        data = {
            'shipping-address-type': constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            'shipping-address-first_name': 'Florent',
            'shipping-address-last_name': 'Messa',
            'shipping-address-city': 'Paris',
            'shipping-address-phone_number': '0183629075',
            'shipping-address-line1': '8 rue saint fiacre',
            'shipping-address-postal_code': '75002',
            'user-email': 'flo@ulule.com',
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302

        data = {
            'shipping-address-type': constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            'shipping-address-first_name': 'Florent',
            'shipping-address-last_name': 'Messa',
            'shipping-address-city': 'Paris',
            'shipping-address-phone_number': '0183629075',
            'shipping-address-line1': '10 rue de montmorency',
            'shipping-address-postal_code': '75002',
            'user-email': 'benoit@ulule.com',
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302

        user = User.objects.filter(email='benoit@ulule.com').first()
        assert user is not None
        assert user.orders.count() == 1

        order = user.orders.first()
        shipping_address = order.shipping_address

        assert shipping_address.line1 == '10 rue de montmorency'


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
