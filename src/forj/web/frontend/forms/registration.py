from django import forms
from django.db import transaction

from forj.forms import MultiModelForm

from .address import AddressForm
from .user import UserForm


class RegistrationForm(MultiModelForm):
    base_forms = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.forms['user'] = UserForm(self.data,
                                      self.files or None,
                                      initial=self.initial,
                                      prefix='user')

        self.forms['shipping_address'] = AddressForm(self.data,
                                                     self.files or None,
                                                     initial=self.initial,
                                                     prefix='shipping-address')

        self.forms['billing_address'] = AddressForm(self.data,
                                                    self.files or None,
                                                    initial=self.initial,
                                                    prefix='billing-address')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            user = self.forms['user'].save()
            shipping_address = self.forms['shipping_address'].save(user=user)
            billing_address = self.forms['billing_address'].save(user=user)
