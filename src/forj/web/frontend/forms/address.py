from django import forms
from django.utils.translation import gettext_lazy as _

from forj.models import Address
from forj.forms import widgets
from forj import constants

import phonenumbers


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'type',
            'first_name',
            'last_name',
            'business_name',
            'line1',
            'line2',
            'postal_code',
            'phone_number',
            'city',
            'country',
        )

        widgets = {
            'line1': forms.TextInput,
            'type': widgets.Radio,
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        country = self.initial.get('country')

        if country is None:
            return value

        try:
            ph = phonenumbers.parse(value, country)

            if not phonenumbers.is_valid_number(ph):
                raise forms.ValidationError(_('Invalid phone number'))

            if not phonenumbers.is_valid_number_for_region(ph, country):
                raise forms.ValidationError(_('Invalid phone number'))
        except phonenumbers.NumberParseException:
            raise forms.ValidationError(_('Invalid phone number'))

        return value

    def save(self, *args, **kwargs):
        self.user = kwargs.pop('user', self.user)
        self.instance.user = self.user

        if self.user:
            self.instance.first_name = self.instance.first_name or self.user.first_name
            self.instance.last_name = self.instance.last_name or self.user.last_name

        return super().save(*args, **kwargs)


class ShippingAddressForm(AddressForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['type'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        if self.data and self.data.get('type') == constants.ADDRESS_TYPE_CHOICES.BUSINESS:
            self.fields['business_name'].required = True
        else:
            self.fields['business_name'].required = False

        self.fields['line1'].required = True
        self.fields['line2'].required = False
        self.fields['city'].required = True
        self.fields['country'].required = True
        self.fields['phone_number'].required = True


class BillingAddressForm(ShippingAddressForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
