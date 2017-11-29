from django.db import models
from django.conf import settings

from forj.db.models import base
from forj import constants

from django_countries.fields import CountryField


class Address(base.Model):
    TYPE_CHOICES = constants.ADDRESS_TYPE_CHOICES

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES,
                                            default=TYPE_CHOICES.INDIVIDUAL,
                                            null=True)

    first_name = models.CharField(max_length=250, verbose_name='First name',
                                  null=True,
                                  blank=True)
    last_name = models.CharField(max_length=250,
                                 verbose_name='Last name',
                                 null=True, blank=True)
    business_name = models.CharField(max_length=250,
                                     verbose_name='Entity name',
                                     null=True, blank=True)
    line1 = models.TextField(verbose_name='Address', null=True)
    line2 = models.TextField(verbose_name='Address 2', null=True, blank=True)
    postal_code = models.CharField(max_length=140,
                                   verbose_name='Postal code',
                                   null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
    city = models.CharField(max_length=140,
                            verbose_name='City',
                            null=True)
    country = CountryField(blank=True, null=True,
                           verbose_name='Country',
                           default=settings.DEFAULT_COUNTRY)

    user = models.ForeignKey('forj.User', related_name='addresses',
                             on_delete=models.PROTECT)

    class Meta:
        abstract = False
        db_table = 'forj_address'

    @property
    def name(self):
        name = ' '.join([self.first_name or '', self.last_name or ''])

        if self.type == self.TYPE_CHOICES.INDIVIDUAL:
            return name

        return '{}\n{}'.format(name, self.business_name)

    @property
    def formatted(self):
        return '%s\n%s\n%s %s\n%s' % (
            self.name or '',
            self.line1 or '',
            self.postal_code or '',
            self.city or '',
            self.get_country_display()
        )
