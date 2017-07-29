forj
====

forj is the personal project of Michel Berard.

Installation
------------

Hosts
.....

Add this lines in your ``/etc/hosts``::

    127.0.0.1       local.forj.com

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

    create user forj with password 'forj';

Then create the database ::

    create database forj with owner forj;

Setup project (models + initial fixtures + index) ::

    make bootstrap
