from django import forms

from .address import RequiredAddressForm, OptionalAddressForm
from .user import UserForm


class RegistrationForm(forms.Form):
    diff = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        self._order = kwargs.pop('order', None)

        country = kwargs.pop('country', None)

        super().__init__(*args, **kwargs)

        self.shipping_address = None
        self.billing_address = None

        if self._order:
            if self._order.shipping_address_id:
                self.shipping_address = self._order.shipping_address

            if self._order.billing_address_id:
                self.billing_address = self._order.billing_address
                self.fields['diff'].initial = True

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

        self.forms = {}

        self.forms['user'] = UserForm(self.data or None,
                                      self.files or None,
                                      initial=self.initial,
                                      instance=self._user,
                                      prefix='user')

        self.forms['shipping_address'] = RequiredAddressForm(self.data or None,
                                                             self.files or None,
                                                             initial=self.initial,
                                                             instance=self.shipping_address,
                                                             prefix='shipping-address')

        billing_address_form_class = OptionalAddressForm

        if self.data.get('diff'):
            billing_address_form_class = RequiredAddressForm

        self.forms['billing_address'] = billing_address_form_class(self.data or None,
                                                                   self.files or None,
                                                                   instance=self.billing_address,
                                                                   initial=self.initial,
                                                                   prefix='billing-address')

        self.forms['billing_address'].fields['phone_number'].required = False

    def is_valid(self):
        return all([form.is_valid() for form in self.forms.values()]) & super().is_valid()

    def save(self, *args, **kwargs):
        user = self.forms['user'].save()
        self.shipping_address = self.forms['shipping_address'].save(user=user)

        if self.cleaned_data.get('diff'):
            self.billing_address = self.forms['billing_address'].save(user=user)
        else:
            self.billing_address = None

        return user
