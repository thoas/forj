import os
import sys

from django import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forje.settings.test')
    setup()
