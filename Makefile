dependencies:
	pip install -r requirements.txt

run-server:
	DJANGO_SETTINGS_MODULE=forj.settings.local python manage.py runserver 127.0.0.1:8181

shell-plus:
	DJANGO_SETTINGS_MODULE=forj.settings.local python manage.py shell_plus

syncdb:
	DJANGO_SETTINGS_MODULE=forj.settings.local python manage.py migrate --run-syncdb

test:
	DJANGO_SETTINGS_MODULE=forj.settings.test python manage.py check
	py.test tests/ -v

bootstrap-db:
	alembic upgrade 314d04a46009

bootstrap: bootstrap-db syncdb initial-data

initial-data:
	DJANGO_SETTINGS_MODULE=forj.settings.local python manage.py loaddata src/forj/fixtures/initial.json

createsuperuser:
	DJANGO_SETTINGS_MODULE=forj.settings.local python manage.py createsuperuser

setup-db:
	psql -U postgres -c "create user forj with password 'forj';"
	psql -U postgres -c "alter role forj with superuser;"
	psql -U postgres -c "create database forj with owner forj;"

destruct-db:
	psql -U postgres -c "drop database forj;"
	psql -d postgres -c "create database forj with owner forj;"

rebuild: destruct-db bootstrap
