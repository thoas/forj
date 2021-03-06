ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUILD_DIR = $(ROOT_DIR)/src/forj/static/site/build

build-translations:
	cd src/forj && pybabel extract -F babel.cfg -o locale/en/LC_MESSAGES/django.po .

compile-translations:
	cd src/forj && django-admin.py compilemessages

outdated:
	pip list -o --format=columns

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
	py.test tests/ -v -s

collectstatic:
	python manage.py collectstatic --noinput -i *.scss --traceback

docker-prebuild:
	docker build -t forj-prebuilder -f Dockerfile.build .
	mkdir -p $(BUILD_DIR)
	docker run --rm -v $(BUILD_DIR):/app/src/forj/static/site/build forj-prebuilder

bootstrap-db:
	alembic upgrade 314d04a46009

bootstrap: bootstrap-db syncdb initial-data

initial-data:
	DJANGO_SETTINGS_MODULE=forj.settings.local python manage.py loaddata src/forj/fixtures/initial.json

createsuperuser:
	DJANGO_SETTINGS_MODULE=forj.settings.local python manage.py createsuperuser

setup-virtualenv:
	pip install pip --upgrade
	pip install virtualenv
	virtualenv .env -p /usr/local/bin/python3

setup-db:
	psql -U postgres -c "create user forj with password 'forj';"
	psql -U postgres -c "alter role forj with superuser;"
	psql -U postgres -c "create database forj with owner forj;"

destruct-db:
	psql -U postgres -c "drop database forj;"
	psql -d postgres -c "create database forj with owner forj;"

rebuild: destruct-db bootstrap

serve-integration:
	cd $(BUILD_DIR) && python3 -m http.server
