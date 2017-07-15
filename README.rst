forje
=====

forje is the personal project of Michel Berrard.

Installation
------------

Hosts
.....

Add this lines in your ``/etc/hosts``::

    127.0.0.1       local.forje.com

Bootstrap
.........

Install the virtualenv

::

    pip install virtualenv
    virtualenv .env
    source .env/bin/activate

Install dependencies

::

    $ make dependencies

Install the database
....................

::

    sudo -u postgres psql

Then create the user ::

    create user forje with password 'forje';

Then create the database ::

    create database forje with owner forje;

Setup project (models + initial fixtures + index) ::

    make bootstrap
