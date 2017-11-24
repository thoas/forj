from django import forms
from django.utils import timezone as datetime
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from forj import exceptions

import stripe


class TextInput(forms.TextInput):
    """
    Inspired by widgets in django-zebra
    """
    def _add_data_stripe_attr(self, name, kwargs):
        kwargs.setdefault('attrs', {}).update({'data-stripe': name})
        return kwargs

    def _strip_name_attr(self, widget_string, name):
        return widget_string.replace("name=\"%s\"" % (name,), "")

    def render(self, name, *args, **kwargs):
        kwargs = self._add_data_stripe_attr(name, kwargs)
        rendered = super().render(name, *args, **kwargs)
        return mark_safe(self._strip_name_attr(rendered, name))


class PaymentForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput(), required=True)

    number = forms.CharField(
        required=False,
        max_length=20,
        label=_('Card number'),
        widget=TextInput(
            attrs={
                'class': 'required first',
                'size': 20,
                'pattern': '\d*',  # number input on mobile
                'autocomplete': 'cc-number',  # for autofill spec
                'tabindex': 2,
            },
        ),
    )
    cvc = forms.CharField(
        required=False,
        label=_('Card security code'),
        widget=TextInput(
            attrs={
                'class': 'required last',
                'size': 4,
                'pattern': '\d*',  # number input on mobile
                'autocomplete': 'off',
                'tabindex': 3,
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order', None)

        super(PaymentForm, self).__init__(*args, **kwargs)

        self.label_suffix = ''

        months = []

        for i in range(12):
            index = i + 1

            months.append((index, ('%d' % index).zfill(2)))

        self.fields['expire_month'] = forms.ChoiceField(choices=(('', (_('Month'))), ) + tuple(months), required=False, widget=forms.Select(attrs={}))

        year = datetime.now().year

        years = list(range(datetime.now().year, year + 20))

        self.fields['expire_year'] = forms.ChoiceField(choices=(('', (_('Year'))), ) + tuple(zip(years, years)), required=False, widget=forms.Select(attrs={}))

    def save(self):
        try:
            charge = stripe.Charge.create(
                amount=self.order.amount,
                currency=self.order.currency,
                source=self.cleaned_data['token'],
                description="order:{}".format(self.order.pk),
                capture=True,
            )
        except stripe.CardError as e:
            raise exceptions.CardError('Invalid card') from e
        except stripe.StripeError as e:
            raise exceptions.PaymentError('Invalid payment') from e

        if charge.status == 'succeeded':
            self.order.mark_as_succeeded(commit=False)
            self.order.stripe_charge = charge
            self.order.save(update_fields=('status', 'stripe_charge', ))
