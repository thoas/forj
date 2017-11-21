from forj.forms import MultiModelForm

from .address import RequiredAddressForm, OptionalAddressForm
from .user import UserForm


class RegistrationForm(MultiModelForm):
    base_forms = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user = kwargs.pop('user', None)
        self._diff = kwargs.pop('diff', None)
        self._order = kwargs.pop('order', None)

        self.shipping_address = None
        self.billing_address = None

        if self._order:
            if self._order.shipping_address_id:
                self.shipping_address = self._order.shipping_address

            if self._order.billing_address_id:
                self.billing_address = self._order.billing_address

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
                                      instance=self._user,
                                      prefix='user')

        self.forms['shipping_address'] = RequiredAddressForm(self.data or None,
                                                             self.files or None,
                                                             initial=self.initial,
                                                             instance=self.shipping_address,
                                                             prefix='shipping-address')

        billing_address_form_class = OptionalAddressForm
        if self._diff:
            billing_address_form_class = RequiredAddressForm

        self.forms['billing_address'] = billing_address_form_class(self.data or None,
                                                                   self.files or None,
                                                                   instance=self.billing_address,
                                                                   initial=self.initial,
                                                                   prefix='billing-address')

    def save(self, *args, **kwargs):
        user = self.forms['user'].save()
        self.shipping_address = self.forms['shipping_address'].save(user=user)

        if self._diff:
            self.billing_address = self.forms['billing_address'].save(user=user)

        return user
