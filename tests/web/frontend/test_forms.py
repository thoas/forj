from forj.utils.test import TestCase
from forj.web.frontend.forms import UserForm, AddressForm, RegistrationForm
from forj.models import Address


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


class RegistrationFormTestCase(TestCase):
    def test_complete(self):
        form = RegistrationForm(data={})
        assert form.is_valid() is False
