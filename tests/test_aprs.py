#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Python APRS-IS Bindings."""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import logging.handlers
import random
import sys
import unittest

import apex.aprs.aprs_internet_service
import apex.aprs.constants

if sys.version_info < (3, 0):
    import httpretty

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '0123456789'
POSITIVE_NUMBERS = NUMBERS[1:]
ALPHANUM = ''.join([ALPHABET, NUMBERS])


class AprsTest(unittest.TestCase):  # pylint: disable=R0904
    """Tests for Python APRS-IS Bindings."""

    logger = logging.getLogger(__name__)
    logger.setLevel(apex.aprs.constants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(apex.aprs.constants.LOG_LEVEL)
    formatter = logging.Formatter(apex.aprs.constants.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False

    @classmethod
    def random(cls, length=8, alphabet=ALPHANUM):
        """
        Generates a random string for test cases.

        :param length: Length of string to generate.
        :param alphabet: Alphabet to use to create string.
        :type length: int
        :type alphabet: str
        """
        return ''.join(random.choice(alphabet) for _ in xrange(length))

    def setUp(self):  # pylint: disable=C0103
        self.fake_server = ''.join([
            'http://localhost:',
            self.random(4, POSITIVE_NUMBERS),
            '/'
        ])

        self.fake_callsign = ''.join([
            self.random(1, 'KWN'),
            self.random(1, NUMBERS),
            self.random(3, ALPHABET),
            '-',
            self.random(1, POSITIVE_NUMBERS)
        ])

        self.real_server = 'http://localhost:14580'
        self.real_callsign = '-'.join(['W2GMD', self.random(1, '123456789')])

        self.logger.debug(
            'fake_server=%s fake_callsign=%s',
            self.fake_server,
            self.fake_callsign
        )

    if sys.version_info < (3, 0):
        @httpretty.httprettified
        def test_fake_good_auth(self):
            """
            Tests authenticating against APRS-IS using a valid call+pass.
            """
            httpretty.HTTPretty.register_uri(
                httpretty.HTTPretty.POST,
                self.fake_server,
                status=204
            )

            aprs_conn = apex.aprs.aprs_internet_service.AprsInternetService(
                user=self.fake_callsign,
                input_url=self.fake_server
            )
            aprs_conn.connect()

            msg = {
                'source': self.fake_callsign,
                'destination': 'APRS',
                'path': ['TCPIP*'],
                'text': '=3745.00N/12227.00W-Simulated Location'
            }
            self.logger.debug(locals())

            result = aprs_conn.send(msg)

            self.assertTrue(result)

        @httpretty.httprettified
        def test_fake_bad_auth_http(self):
            """
            Tests authenticating against APRS-IS using an invalid call+pass.
            """
            httpretty.HTTPretty.register_uri(
                httpretty.HTTPretty.POST,
                self.fake_server,
                status=401
            )

            aprs_conn = apex.aprs.aprs_internet_service.AprsInternetService(
                user=self.fake_callsign,
                input_url=self.fake_server
            )
            aprs_conn.connect()

            msg = {
                'source': self.fake_callsign,
                'destination': 'APRS',
                'path': ['TCPIP*'],
                'text': '=3745.00N/12227.00W-Simulated Location'
            }
            self.logger.debug(locals())

            result = aprs_conn.send(msg, protocol='HTTP')

            self.assertFalse(result)

        @unittest.skip('Test only works with real server.')
        def test_more(self):
            """
            Tests APRS-IS binding against a real APRS-IS server.
            """
            aprs_conn = apex.aprs.aprs_internet_service.AprsInternetService(
                user=self.real_callsign,
                input_url=self.real_server
            )
            aprs_conn.connect()

            msg = {
                'source': self.fake_callsign,
                'destination': 'APRS',
                'path': ['TCPIP*'],
                'text': '=3745.00N/12227.00W-Simulated Location'
            }
            self.logger.debug(locals())

            result = aprs_conn.send(msg)

            self.assertFalse(result)
