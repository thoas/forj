import os
import jinja2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = lambda *a: os.path.join(BASE_DIR, *a)  # noqa
DEPENDENCY_PATH = os.path.join(os.path.dirname(jinja2.__file__), os.pardir)

SECRET_KEY = 'pn442e6ha)cvkme3mz^$5e(3f0y=8@cdlg-k&0onv2$t@i*68j'

DEBUG = True

ALLOWED_HOSTS = [
    '.forj.com',
]

AUTH_USER_MODEL = 'forj.User'
DEFAULT_COUNTRY = 'FR'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forj',
    'django_extensions',
    'easy_thumbnails',
    'django_jinja',
    'django_jinja.contrib._easy_thumbnails',
    'django_jinja.contrib._humanize',
    'django_hosts',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_HOSTCONF = 'forj.hosts'
DEFAULT_HOST = 'www'
PARENT_HOST = 'local.forj.com'

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_COOKIE_NAME = 'fj_session'
SESSION_COOKIE_DOMAIN = '.forj.com'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CSRF_COOKIE_DOMAIN = '.forj.com'

DEFAULT_FROM_EMAIL = 'contact@forj.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

ROOT_URLCONF = 'forj.web.frontend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(DEPENDENCY_PATH, 'debug_toolbar', 'templates'),
            os.path.join(DEPENDENCY_PATH, 'django', 'contrib', 'admin', 'templates'),
            os.path.join(DEPENDENCY_PATH, 'django', 'contrib', 'auth', 'templates'),
            os.path.join(DEPENDENCY_PATH, 'django', 'forms', 'templates'),
            path('djtemplates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        'DIRS': [
            path('templates'),
            os.path.join(DEPENDENCY_PATH, 'django', 'forms', 'jinja2'),
        ],
        "OPTIONS": {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            # Match the template names ending in .html but not the ones in the admin folder.
            "match_extension": ".html",
            "match_regex": r"^(?!admin/).*",
            "app_dirname": "templates",

            # Can be set to "jinja2.Undefined" or any other subclass.
            "undefined": None,
            "newstyle_gettext": True,
            "filters": {
            },
            "globals": {
            },
            "constants": {
            },
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
            ],
            "bytecode_cache": {
                "name": "default",
                "backend": "django_jinja.cache.BytecodeCache",
                "enabled": False,
            },
            "autoescape": True,
            "auto_reload": True,
            "translation_engine": "django.utils.translation",
        }
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'forj',
        'USER': 'forj',
        'PASSWORD': 'forj',
        'HOST': '127.0.0.1',
        'PORT': '',
        'TEST_NAME': 'forj_test'
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Europe/Paris'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

AUTHENTIFICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
