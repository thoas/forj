import importlib

from django import test
from django.utils.lru_cache import lru_cache
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from exam import Exam, fixture


@lru_cache()
def get_session_store():
    settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
    engine = importlib.import_module('django.contrib.sessions.backends.file')
    store = engine.SessionStore()
    store.save()

    return store


class TestCase(Exam, test.TestCase):
    @fixture
    def anonymous(self):
        return AnonymousUser()

    @fixture
    def session_store(self):
        return get_session_store()
