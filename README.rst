=============================
django-filer-celery
=============================

.. image:: https://img.shields.io/pypi/v/django-filer-celery.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-filer-celery
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-filer-celery.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-filer-celery
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/django-filer-celery.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-filer-celery
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/django-filer-celery.svg?style=flat-square
    :target: https://travis-ci.org/nephila/django-filer-celery
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/django-filer-celery/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-filer-celery?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/django-filer-celery/develop.svg?style=flat-square
    :target: https://codecov.io/github/nephila/django-filer-celery
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/django-filer-celery/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-filer-celery
   :alt: Code Climate


Celery powered django-filer tasks and templatetags

Documentation
-------------

The full documentation is at https://django-filer-celery.readthedocs.io.

Quickstart
----------

Install django-filer-celery::

    pip install django-filer-celery

Then add to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'filer_celery',
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python setup.py test

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage-helper`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage-helper`: https://github.com/nephila/cookiecutter-djangopackage-helper
