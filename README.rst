========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - support
      - |docs| |gitter|
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

.. |coveralls| image:: https://coveralls.io/repos/github/Syncleus/apex/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/Syncleus/apex?branch=master

.. |codecov| image:: https://codecov.io/github/Syncleus/apex/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Syncleus/apex

.. |landscape| image:: https://landscape.io/github/Syncleus/apex/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Syncleus/apex/master
    :alt: Code Quality Status

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/4d662dc79744416b950273fb57a64d6e
    :target: https://www.codacy.com/app/freemo/apex?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Syncleus/apex&amp;utm_campaign=Badge_Grade
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/Syncleus/apex/badges/gpa.svg
   :target: https://codeclimate.com/github/Syncleus/apex
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/apex-radio.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/apex-radio

.. |downloads| image:: https://img.shields.io/pypi/dm/apex-radio.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/apex-radio

.. |wheel| image:: https://img.shields.io/pypi/wheel/apex-radio.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/apex-radio

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/apex-radio.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/apex-radio

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/apex-radio.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/apex-radio

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/Syncleus/apex/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/Syncleus/apex/

.. |gitter| image:: https://badges.gitter.im/Syncleus/APEX.svg
   :alt: Join the chat at https://gitter.im/Syncleus/APEX
   :target: https://gitter.im/Syncleus/APEX?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


.. end-badges

APEX is a next generation APRS based protocol. This repository represents the reference implementation and is a full features application for digipeating across multiple AX.25 KISS TNC devices using the full APEX stack.

For more information on the project please check out `the project's home page <http://apexprotocol.com/>`_.

Installation
============

Install the application using pip.

    pip install apex-radio

Running the app
===============

The application is written for python 2 or 3. Once installed copy the apex.conf.example file over to apex.conf in the
/etc directory, then edit the file and replace it with your details. Next just run the application with the following
command.

    apex -v

There isn't much to the application right now, so thats all you should need to run it. Digipeating will occur
automatically and respond to the WIDEN-n paradigm as well as your own callsign. Cross-band repeating is enabled right
now but only by specifying the call sign directly. The application is still pre-release so more features and
configuration options should be added soon.

This is Free software: Apache License v2

Documentation
=============

https://apex.readthedocs.io/

Development
===========

Initial setup::

    pip install -U pyenv tox
    pyenv install 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1
    pyenv global 2.7 3.3.6 3.4.5 3.5.2 pypy-5.4.1

NOTE: The specific versions mentioned above may be different for each platform. use `pyenv install --list` to view the
list of available versions. You will need a version of 2.7.x, 3.3.x, 3.4.x, 3.5.x, and pypy. Try to use the latest
available version for each. Also some flavors of pyenv have different formats for it's arguments. So read the pyenv
documentation on your platform.

To run all tests::

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

