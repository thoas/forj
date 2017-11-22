from jinja2.ext import Extension

from . import filters


class ForjExtension(Extension):
    def __init__(self, environment):
        environment.filters['amount'] = filters.amount
