from django import forms
from django.utils.crypto import get_random_string

from forj.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].required = False

    def save(self, *args, **kwargs):
        if not self.instance.password:
            self.instance.password = get_random_string()

        return super().save(*args, **kwargs)
