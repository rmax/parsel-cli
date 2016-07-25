==========
Parsel CLI
==========

.. image:: https://img.shields.io/pypi/v/parsel-cli.svg
        :target: https://pypi.python.org/pypi/parsel-cli

.. image:: https://img.shields.io/pypi/pyversions/parsel-cli.svg
        :target: https://pypi.python.org/pypi/parsel-cli

.. image:: https://readthedocs.org/projects/parsel-cli/badge/?version=latest
        :target: https://readthedocs.org/projects/parsel-cli/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/travis/rolando/parsel-cli.svg
        :target: https://travis-ci.org/rolando/parsel-cli

.. image:: https://codecov.io/github/rolando/parsel-cli/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/rolando/parsel-cli

.. image:: https://landscape.io/github/rolando/parsel-cli/master/landscape.svg?style=flat
    :target: https://landscape.io/github/rolando/parsel-cli/master
    :alt: Code Quality Status

.. image:: https://requires.io/github/rolando/parsel-cli/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/rolando/parsel-cli/requirements/?branch=master

Parsel Command Line Interface

* Free software: MIT license
* Documentation: https://parsel-cli.readthedocs.org.
* Python versions: 2.7, 3.4+

Quickstart
----------

Example::

    $ curl http://scrapy.org/ | parsel-cli '.container a::attr(href)' | tail -2
    http://doc.scrapy.org/en/latest/topics/ubuntu.html
    https://github.com/scrapy/scrapy/archive/1.1.zip


See ``parsel-cli -h`` for more options.


Credits
-------

This package was created with Cookiecutter_ and the `rolando/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`rolando/cookiecutter-pypackage`: https://github.com/rolando/cookiecutter-pypackage
