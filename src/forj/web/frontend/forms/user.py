from django import forms
from django.utils.crypto import get_random_string

from forj.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def save(self, *args, **kwargs):
        self.instance.password = get_random_string()

        return super().save(*args, **kwargs)
