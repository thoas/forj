import json  # noqa

from forj.models import Product


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Product):
            return obj.serialized_data

        return super(JSONEncoder, self).default(obj)
