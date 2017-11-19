from django.conf import settings

from forj.utils.test import TestCase
from forj.web.frontend.forms import UserForm, AddressForm, RegistrationForm, RequiredAddressForm
from forj.models import Address, User
from forj import constants


class UserFormTestCase(TestCase):
    def test_complete(self):
        form = UserForm(data={
            'first_name': 'Florent',
            'last_name': 'Messa',
            'email': 'florent@forj.com',
        })

        assert form.is_valid() is True

        user = form.save()

        assert user is not None

    def test_email_exists(self):
        form = UserForm(data={
            'first_name': 'Florent',
            'last_name': 'Messa',
            'email': self.user.email,
        })

        assert form.is_valid() is False
        assert 'email' in form.errors


class AddressFormTestCase(TestCase):
    def test_complete(self):
        form = AddressForm(data={
            'line1': '8 rue saint fiacre',
            'postal_code': '75002',
            'city': 'Paris',
            'phone_number': '0183629075',
            'type': Address.TYPE_CHOICES.BUSINESS,
        }, initial={'country': 'FR'}, user=self.user)

        assert form.is_valid() is True

        address = form.save()

        assert address is not None
        assert address.user_id == self.user.pk

    def test_invalid(self):
        form = AddressForm(data={
            'line1': '8 rue saint fiacre',
            'postal_code': '75002',
            'city': 'Paris',
            'phone_number': '00000000',
            'type': Address.TYPE_CHOICES.BUSINESS,
        }, initial={'country': 'FR'}, user=self.user)

        assert form.is_valid() is False
        assert 'phone_number' in form.errors


class RequiredAddressFormTestCase(TestCase):
    def test_complete_business(self):
        form = RequiredAddressForm(data={
            'line1': '8 rue saint fiacre',
            'postal_code': '75002',
            'city': 'Paris',
            'country': 'FR',
            'phone_number': '0183629075',
            'type': Address.TYPE_CHOICES.BUSINESS,
        }, user=self.user)

        assert form.is_valid() is False
        assert 'first_name' in form.errors
        assert 'last_name' in form.errors
        assert 'business_name' in form.errors

    def test_complete(self):
        form = RequiredAddressForm(data={
            'line1': '8 rue saint fiacre',
            'postal_code': '75002',
            'city': 'Paris',
            'first_name': 'Florent',
            'last_name': 'Messa',
            'country': 'FR',
            'phone_number': '0183629075',
            'type': Address.TYPE_CHOICES.INDIVIDUAL,
        }, user=self.user)

        assert form.is_valid() is True


class RegistrationFormTestCase(TestCase):
    def test_simple(self):
        form = RegistrationForm(data={'foo': 'bar'})
        assert form.is_valid() is False

    @property
    def address_data(self):
        return {
            'type': constants.ADDRESS_TYPE_CHOICES.INDIVIDUAL,
            'first_name': 'Florent',
            'last_name': 'Messa',
            'city': 'Paris',
            'phone_number': '0183629075',
            'line1': '8 rue saint fiacre',
            'postal_code': '75002',
        }

    @property
    def data(self):
        email = 'flo@ulule.com'

        shipping_data = self.address_data

        data = {
            'user-email': email,
        }

        for k, v in shipping_data.items():
            data['shipping-address-{}'.format(k)] = v

        return data

    def test_complete(self):
        form = RegistrationForm(data=self.data,
                                country=settings.DEFAULT_COUNTRY)

        assert form.is_valid() is True

        user = form.save()

        assert user.pk is not None
        assert User.objects.filter(email=self.data['user-email']).count() == 1
        assert user.addresses.count() == 1

        shipping_address = user.addresses.first()

        for k, v in self.address_data.items():
            assert getattr(shipping_address, k) == v

    def test_complete_billing(self):
        data = self.data

        form = RegistrationForm(data=data,
                                diff=True,
                                country=settings.DEFAULT_COUNTRY)

        assert form.is_valid() is False

        for k, v in self.address_data.items():
            data['billing-address-{}'.format(k)] = v

        form = RegistrationForm(data=data,
                                diff=True,
                                country=settings.DEFAULT_COUNTRY)

        assert form.is_valid() is True

        user = form.save()

        assert user.pk is not None
        assert User.objects.filter(email=self.data['user-email']).count() == 1
        assert user.addresses.count() == 2
