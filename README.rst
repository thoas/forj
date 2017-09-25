forj
====

.. image:: https://secure.travis-ci.org/thoas/forj.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/forj


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

Then setup the database ::

    make setup-db

Setup project (models + initial fixtures + index) ::

    make bootstrap
