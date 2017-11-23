from django import forms
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from forj.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False

    def clean_email(self):
        value = self.cleaned_data['email']

        qs = User.objects.filter(email=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(_('This email already exists'))

        return value

    def save(self, *args, **kwargs):
        if not self.instance.password:
            self.instance.set_password(get_random_string())

        return super().save(*args, **kwargs)
