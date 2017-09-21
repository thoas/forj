from django.db import models
from django.utils import timezone as datetime


class QuerySet(models.QuerySet):
    pass


class Manager(models.Manager):
    def get_queryset(self):
        return QuerySet(self.model)


class Model(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Manager()

    class Meta:
        abstract = True
