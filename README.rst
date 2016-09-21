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

.. |docs| image:: https://readthedocs.org/projects/apex/badge/?version=latest
    :target: http://apex.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/Syncleus/apex.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Syncleus/apex

.. |requires| image:: https://requires.io/github/Syncleus/apex/requirements.svg?branch=master
     :alt: Requirements Status
     :target: https://requires.io/github/Syncleus/apex/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/Syncleus/apex/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/Syncleus/apex

.. |codecov| image:: https://codecov.io/github/Syncleus/apex/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Syncleus/apex

.. |landscape| image:: https://landscape.io/github/Syncleus/apex/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Syncleus/apex/master
    :alt: Code Quality Status

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/4d662dc79744416b950273fb57a64d6e
    :target: https://www.codacy.com/app/freemo/apex?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Syncleus/apex&amp;utm_campaign=Badge_Grade
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

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/Syncleus/apex/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/Syncleus/apex/


.. end-badges

APEX is a next generation APRS based protocol. This repository represents the reference implementation and is a full features application for digipeating across multiple AX.25 KISS TNC devices using the full APEX stack.

For more information on the project please check out [the project's home page](http://apexprotocol.com/).

Running the app
===============

Right now the setup.py has a few bugs in it. So you can either try to fix it, wait for us to fix it, or simply install
the prerequsites manually. The following is a list of the preequsites that need to be installed.

    pynmea2 >= 1.4.2
    pyserial >= 2.7
    requests >= 2.7.0
    cachetools >= 1.1.5

The application is written for python 3 specifically, it may not work with python 2. Once installed copy the
apex.cfg.example file over to apex.cfg in the same directory, then edit the file and replace it with your details. Next
just run the application with the following command.

    python ./apex.py

There isnt much to the application right now, so thats all you should need to run it. Digipeating will occur
automatically and respond to the WIDEN-n paradigm as well as your own callsign. Cross-band repeating is enabled right
now but only by specifying the call sign directly. The application is still pre-release so more features and
configuration options should be added soon.

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

    pip install -U pyenv tox flake8 httpretty
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
