from django import forms


class AmountField(forms.FloatField):
    def prepare_value(self, value):
        if value:
            value = float(value) / 100.0

        return super().prepare_value(value)

    def to_python(self, value):
        value = super().to_python(value)

        if value:
            return int(value * 100.0)

        return value
