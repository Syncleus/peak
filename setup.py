#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the APEX Python Module.

Source:: https://github.com/syncleus/apex
"""


__title__ = 'apex'
__version__ = '0.0.1'
__author__ = 'Jeffrey Phillips Freeman WI2ARD <freemo@gmail.com>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'


import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=F0401,E0611


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setup(
    name='apex',
    version=__version__,
    description='Python Library for APRS.',
    author='Jeffrey Phillips Freeman',
    author_email='freemo@gmail.com',
    packages=['apex'],
    package_data={'': ['LICENSE']},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/syncleus/apex',
    setup_requires=[
      'coverage >= 3.7.1',
      'httpretty >= 0.8.10',
      'nose >= 1.3.7'
    ],
    install_requires=[
        'pynmea2 >= 1.4.2',
        'pyserial >= 2.7',
        'requests >= 2.7.0',
        'MySQLdb >= 1.2.5',
        'mysql >= 2.1.3'
    ],
    package_dir={'apex': 'apex'},
    zip_safe=False,
    include_package_data=True,
    entry_points={'console_scripts': ['aprs_tracker = aprs.cmd:tracker']}
)
