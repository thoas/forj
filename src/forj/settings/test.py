from .local import *  # noqa

SILENCED_SYSTEM_CHECKS = [
    '1_6.W002',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'forj_test',
        'USER': 'forj',
        'PASSWORD': 'forj',
        'HOST': '127.0.0.1',
        'PORT': '',
        'TEST_NAME': 'forj_test'
    }
}
