from django.db import transaction

from forj.forms import MultiModelForm

from .address import RequiredAddressForm, OptionalAddressForm
from .user import UserForm


class RegistrationForm(MultiModelForm):
    base_forms = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user = kwargs.pop('user', None)
        self._diff = kwargs.pop('diff', None)

        country = kwargs.pop('country', None)

        if country is not None:
            self.initial = {
                'shipping-address-country': country,
                'billing-address-country': country,
            }

            if self.data:
                data = self.data.copy()

                data['shipping-address-country'] = country
                data['billing-address-country'] = country

                self.data = data

        self.forms['user'] = UserForm(self.data or None,
                                      self.files or None,
                                      initial=self.initial,
                                      prefix='user')

        self.forms['shipping_address'] = RequiredAddressForm(self.data or None,
                                                             self.files or None,
                                                             initial=self.initial,
                                                             prefix='shipping-address')

        billing_address_form_class = OptionalAddressForm
        if self._diff:
            billing_address_form_class = RequiredAddressForm

        self.forms['billing_address'] = billing_address_form_class(self.data or None,
                                                                   self.files or None,
                                                                   initial=self.initial,
                                                                   prefix='billing-address')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            user = self.forms['user'].save()
            self.forms['shipping_address'].save(user=user)

            if self._diff:
                self.forms['billing_address'].save(user=user)

            return user
