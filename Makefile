dependencies:
	pip install -r requirements.txt

runserver:
	DJANGO_SETTINGS_MODULE=forje.settings.local python manage.py runserver 127.0.0.1:8181

shell_plus:
	DJANGO_SETTINGS_MODULE=forje.settings.local python manage.py shell_plus

syncdb:
	DJANGO_SETTINGS_MODULE=forje.settings.local python manage.py migrate --run-syncdb

test:
	DJANGO_SETTINGS_MODULE=forje.settings.test python manage.py check
	py.test tests/ -v
