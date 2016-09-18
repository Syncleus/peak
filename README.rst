========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/apex/badge/?style=flat
    :target: https://readthedocs.org/projects/apex
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/syncleus/apex.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/syncleus/apex

.. |requires| image:: https://requires.io/github/syncleus/apex/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/syncleus/apex/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/syncleus/apex/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/syncleus/apex

.. |codecov| image:: https://codecov.io/github/syncleus/apex/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/syncleus/apex

.. |landscape| image:: https://landscape.io/github/syncleus/apex/master/landscape.svg?style=flat
    :target: https://landscape.io/github/syncleus/apex/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg?style=flat
    :target: https://www.codacy.com/app/syncleus/apex
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/syncleus/apex/badges/gpa.svg
   :target: https://codeclimate.com/github/syncleus/apex
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/apex.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/apex

.. |downloads| image:: https://img.shields.io/pypi/dm/apex.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/apex

.. |wheel| image:: https://img.shields.io/pypi/wheel/apex.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/apex

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/apex.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/apex

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/apex.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/apex

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/syncleus/apex/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/syncleus/apex/


.. end-badges

APEX reference implementation

* Free software: BSD license

Installation
============

::

    pip install apex

Documentation
=============

https://apex.readthedocs.io/

Development
===========

Initial setup::

    pip install -U pyenv tox
    pyenv install 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1
    pyenv global 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
