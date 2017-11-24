from django.db import models


class ReverseSingleRelatedObjectDescriptor(object):
    def __init__(self, field_with_rel):
        self.field = field_with_rel

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        cache_name = self.field.get_cache_name()
        try:
            return getattr(instance, cache_name)
        except AttributeError:
            val = getattr(instance, self.field.attname)
            if val is None:
                # If NULL is an allowed value, return it.
                if self.field.null:
                    return None

            rel_obj = self.field.methods['get'](instance, val, self.field)

            setattr(instance, cache_name, rel_obj)

            return rel_obj

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("%s must be accessed via instance" % self._field.name)

        if value is None and self.field.null is False:
            raise ValueError('Cannot assign None: "%s.%s" does not allow null values.' %
                             (instance._meta.object_name, self.field.name))
        elif value is not None and not isinstance(value, self.field.to):
            raise ValueError('Cannot assign "%r": "%s.%s" must be a "%s" instance.' %
                             (value, instance._meta.object_name,
                              self.field.name, self.field.to))

        setattr(instance, self.field.attname, value.id)

        setattr(instance, self.field.get_cache_name(), value)


def create_resource(instance, **parameters):
    return instance.resource_field.to.create(**parameters)


def retrieve_resource(instance, value, field):
    return field.to.retrieve(value)


def update_resource(instance):
    instance.resource.save()
    return instance.resource


class ResourceField(models.CharField):
    def __init__(self, to=None, methods=None, *args, **kwargs):
        kwargs['max_length'] = 100

        super(ResourceField, self).__init__(*args, **kwargs)

        self.to = to
        self.methods = {
            'get': retrieve_resource,
            'create': create_resource,
            'update': update_resource
        }
        if methods is not None:
            self.methods.update(methods)

    def get_attname(self):
        return '%s_id' % self.name

    def get_cache_name(self):
        return '%s_cache' % self.name

    def contribute_to_class(self, cls, name):
        super(ResourceField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, ReverseSingleRelatedObjectDescriptor(self))
