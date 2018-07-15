from django.db import models

from forj.forms import fields


class AmountField(models.PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        self.ndigits = kwargs.pop("ndigits", 2)

        super(AmountField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super(AmountField, self).contribute_to_class(cls, name, **kwargs)

        setattr(
            cls, "%s_converted" % self.name, AmountDescriptor(self.name, self.ndigits)
        )

    def formfield(self, **kwargs):
        defaults = {"form_class": fields.AmountField}
        defaults.update(kwargs)
        return super(AmountField, self).formfield(**defaults)


class AmountDescriptor(object):
    def __init__(self, name, ndigits):
        self.field_name = name
        self.ndigits = ndigits

    def __get__(self, instance, instance_type=None):
        value = getattr(instance, self.field_name)

        if value is not None:
            amount = round(value / 100.0, self.ndigits)

            if amount % 1 == 0.0:
                return int(amount)

            return amount

        return None

    def __set__(self, instance, value):
        setattr(instance, self.field_name, int(value * 100))
