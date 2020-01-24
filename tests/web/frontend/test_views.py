from forj.utils.test import TestCase
from forj import constants
from forj.models import Order, Address

from django.urls import reverse
from django.core import mail

from exam import fixture, before


class HomeTest(TestCase):
    @fixture
    def path(self):
        return reverse("home")

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200


class CheckoutTest(TestCase):
    @fixture
    def path(self):
        return reverse("checkout")

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 302

    def test_complete(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)
        self.cart.add_product("LA(37)-LO(50)-H(50)", 1)

        self.cart.to_request(self.client)

        response = self.client.get(self.path)

        assert response.status_code == 200

        data = {
            "shipping-address-type": constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            "shipping-address-first_name": "Florent",
            "shipping-address-last_name": "Messa",
            "shipping-address-email": "florent@forj.com",
            "shipping-address-city": "Paris",
            "shipping-address-phone_number": "0183629075",
            "shipping-address-line1": "8 rue saint fiacre",
            "shipping-address-postal_code": "75002",
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302

        assert "_order_id" in self.client.session

        order = Order.objects.filter(pk=self.client.session["_order_id"]).first()
        assert order is not None
        assert response["Location"] == order.get_payment_url()
        assert order.shipping_address_id is not None


class CheckoutUpdateTest(TestCase):
    @fixture
    def order(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)
        self.cart.add_product("LA(37)-LO(50)-H(50)", 1)

        order = self.cart.save()

        return order

    @property
    def path(self):
        return self.order.get_checkout_url()

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 302

    def test_update_remove_billing(self):
        self.cart.to_request(self.client)

        data = {
            "shipping-address-type": constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            "shipping-address-first_name": "Florent",
            "shipping-address-last_name": "Messa",
            "shipping-address-city": "Paris",
            "shipping-address-phone_number": "0183629075",
            "shipping-address-line1": "8 rue saint fiacre",
            "shipping-address-postal_code": "75002",
            "shipping-address-email": "flo@ulule.com",
            "diff": 1,
            "billing-address-type": constants.ADDRESS_TYPE_CHOICES.BUSINESS,
            "billing-address-first_name": "Florent",
            "billing-address-last_name": "Messa",
            "billing-address-email": "flo@ulule.com",
            "billing-address-business_name": "Ulule",
            "billing-address-city": "Paris",
            "billing-address-phone_number": "0183629075",
            "billing-address-line1": "8 rue saint fiacre",
            "billing-address-postal_code": "75002",
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302
        assert "_order_id" in self.client.session
        order = Order.objects.get(pk=self.client.session["_order_id"])

        assert order.billing_address_id is not None
        assert order.shipping_address_id is not None

        data = {
            "shipping-address-type": constants.ADDRESS_TYPE_CHOICES.BUSINESS,
            "shipping-address-first_name": "Florent",
            "shipping-address-last_name": "Messa",
            "shipping-address-business_name": "Ulule",
            "shipping-address-city": "Paris",
            "shipping-address-phone_number": "0183629075",
            "shipping-address-line1": "8 rue saint fiacre",
            "shipping-address-postal_code": "75002",
            "shipping-address-email": "flo@ulule.com",
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302

        order = Order.objects.get(pk=self.order.pk)

        assert order.billing_address_id is None
        assert order.shipping_address_id is not None

    def test_update(self):
        self.cart.to_request(self.client)

        data = {
            "shipping-address-type": constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            "shipping-address-first_name": "Florent",
            "shipping-address-last_name": "Messa",
            "shipping-address-city": "Paris",
            "shipping-address-phone_number": "0183629075",
            "shipping-address-line1": "8 rue saint fiacre",
            "shipping-address-postal_code": "75002",
            "shipping-address-email": "flo@ulule.com",
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302
        assert "_order_id" in self.client.session
        order = Order.objects.get(pk=self.client.session["_order_id"])

        data = {
            "shipping-address-type": constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            "shipping-address-first_name": "Florent",
            "shipping-address-last_name": "Messa",
            "shipping-address-city": "Paris",
            "shipping-address-phone_number": "0183629075",
            "shipping-address-line1": "10 rue de montmorency",
            "shipping-address-postal_code": "75002",
            "shipping-address-email": "benoit@ulule.com",
        }

        response = self.client.post(self.path, data=data)

        assert response.status_code == 302

        shipping_address = order.shipping_address

        assert shipping_address.line1 == "10 rue de montmorency"


class PaymentTest(TestCase):
    @fixture
    def path(self):
        return reverse("payment", args=[self.order.reference])

    def test_redirect(self):
        self.order.mark_as_succeeded()

        response = self.client.get(self.path)

        assert response.status_code == 302
        assert response["Location"] == self.order.get_success_url()


class SuccessTest(TestCase):
    @fixture
    def path(self):
        return reverse("success", args=[self.order.reference])

    def test_permission(self):
        response = self.client.get(self.path)

        assert response.status_code == 404

    def test_view(self):
        self.order.mark_as_succeeded()

        response = self.client.get(self.path)

        assert response.status_code == 200
        assert len(mail.outbox) == 1


class CartTest(TestCase):
    @fixture
    def path(self):
        return reverse("cart")

    def test_view(self):
        response = self.client.get(self.path, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        assert response.status_code == 200

        response = self.client.get("{}?next=checkout".format(self.path))

        assert response.status_code == 302
        assert response["Location"] == reverse("checkout")

    def test_add(self):
        response = self.client.post(
            self.path,
            data={"reference": "LA(37)-LO(122)-H(67)", "action": "add"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        assert response.status_code == 200
        assert response.content is not None

        content = response.json()

        assert len(content["items"]) == 1

        entry = content["items"][0]

        assert entry["quantity"] == 1
        assert entry["reference"] == "LA(37)-LO(122)-H(67)"
        assert content["total"] == 54300
        assert content["amount"] == 54300
        assert content["shipping_cost"] == 0

        response = self.client.post(
            self.path,
            data={"reference": "LA(37)-LO(122)-H(67)", "action": "add"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        content = response.json()

        assert len(content["items"]) == 1

        entry = content["items"][0]

        assert entry["quantity"] == 2

    def test_remove(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)

        self.cart.to_request(self.client)

        response = self.client.get(self.path, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        assert response.status_code == 200

        content = response.json()

        assert len(content["items"]) == 1
        entry = content["items"][0]
        assert entry["quantity"] == 1

        response = self.client.post(
            self.path,
            data={"reference": "LA(37)-LO(122)-H(67)", "action": "remove"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        assert response.status_code == 200

        content = response.json()

        assert len(content["items"]) == 0
        assert content["amount"] == 0
        assert content["total"] == 0
        assert content["shipping_cost"] == 0


class CollectionTest(TestCase):
    @fixture
    def path(self):
        return reverse("collection")

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200


class InvoiceTest(TestCase):
    @fixture
    def order(self):
        self.cart.add_product("LA(37)-LO(122)-H(67)", 1)

        order = self.cart.save()
        order.shipping_address = Address.objects.create(email="florent@forj.shop")
        order.mark_as_succeeded()

        return order

    @fixture
    def path(self):
        return self.order.get_invoice_url()

    def test_view(self):
        response = self.client.get(self.path)

        assert response.status_code == 200
