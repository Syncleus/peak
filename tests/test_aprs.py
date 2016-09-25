#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Python APRS-IS Bindings."""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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

DECODED_CALLSIGN = callsign = {'callsign': 'W2GMD', 'ssid': 1}
ENCODED_CALLSIGN = [174, 100, 142, 154, 136, 64, 98]

DECODED_CALLSIGN_DIGIPEATED = {'callsign': 'W2GMD*', 'ssid': 1}
ENCODED_CALLSIGN_DIGIPEATED = [174, 100, 142, 154, 136, 64, 226]

DECODED_FRAME = {
            'source': 'W2GMD-1',
            'destination': 'OMG',
            'path': ['WIDE1-1'],
            'text': 'test_encode_frame'
        }
ENCODED_FRAME = [158, 154, 142, 64, 64, 64, 96, 174, 100, 142, 154, 136, 64, 98, 174, 146, 136, 138, 98, 64, 99, 3, 240,
                 116, 101, 115, 116, 95, 101, 110, 99, 111, 100, 101, 95, 102, 114, 97, 109, 101]

DECODED_FRAME_RECORDED = {
            'source': 'W2GMD-6',
            'destination': 'APRX24',
            'path': ['WIDE1-1'],
            'text': ('!3745.75NI12228.05W#W2GMD-6 Inner Sunset, '
                     'SF iGate/Digipeater http://w2gmd.org')
        }
ENCODED_FRAME_RECORDED = [130, 160, 164, 176, 100, 104, 96, 174, 100, 142, 154, 136, 64, 108, 174, 146, 136, 138, 98,
                          64, 99, 3, 240, 33, 51, 55, 52, 53, 46, 55, 53, 78, 73, 49, 50, 50, 50, 56, 46, 48, 53, 87,
                          35, 87, 50, 71, 77, 68, 45, 54, 32, 73, 110, 110, 101, 114, 32, 83, 117, 110, 115, 101, 116,
                          44, 32, 83, 70, 32, 105, 71, 97, 116, 101, 47, 68, 105, 103, 105, 112, 101, 97, 116, 101, 114,
                          32, 104, 116, 116, 112, 58, 47, 47, 119, 50, 103, 109, 100, 46, 111, 114, 103]

DECODED_FRAME_MULTIPATH = {
            'source': 'W2GMD-1',
            'destination': 'OMG',
            'path': ['WIDE1-1', 'WIDE2-2'],
            'text': 'test_encode_frame'
        }
ENCODED_FRAME_MULTIPATH = [158, 154, 142, 64, 64, 64, 96, 174, 100, 142, 154, 136, 64, 98, 174, 146, 136, 138, 98, 64,
                           98, 174, 146, 136, 138, 100, 64, 101, 3, 240, 116, 101, 115, 116, 95, 101, 110, 99, 111, 100,
                           101, 95, 102, 114, 97, 109, 101]


class AprsTest(unittest.TestCase):  # pylint: disable=R0904
    """Tests for Python APRS-IS Bindings."""

    def setUp(self):  # pylint: disable=C0103
        self.fake_server = 'http://localhost:5567/'
        self.fake_callsign = 'KWN4YGH-5'

    def test_encode_callsign(self):
        """
        Tests encoding a callsign.
        """
        encoded_callsign = apex.aprs.Aprs._Aprs__encode_callsign(DECODED_CALLSIGN)
        self.assertEqual(ENCODED_CALLSIGN, encoded_callsign)

    def test_encode_callsign_digipeated(self):
        """
        Tests encoding a digipeated callsign with
        `aprs.util.encode_callsign()`.
        """
        encoded_callsign = apex.aprs.Aprs._Aprs__encode_callsign(DECODED_CALLSIGN_DIGIPEATED)
        self.assertEqual(ENCODED_CALLSIGN_DIGIPEATED, encoded_callsign)

    def test_decode_callsign(self):
        """
        Tests extracting the callsign from a KISS-encoded APRS frame.
        """
        decoded_callsign = apex.aprs.Aprs._Aprs__extract_callsign(ENCODED_CALLSIGN)
        self.assertEqual(DECODED_CALLSIGN, decoded_callsign)

    def test_decode_callsign_digipeated(self):
        """
        Tests extracting the callsign from a KISS-encoded APRS frame.
        """
        decoded_callsign = apex.aprs.Aprs._Aprs__extract_callsign(ENCODED_CALLSIGN_DIGIPEATED)
        self.assertEqual(DECODED_CALLSIGN, decoded_callsign)

    def test_encode_frame(self):
        """
        Tests KISS-encoding an APRS.
        """
        encoded_frame = apex.aprs.Aprs._Aprs__encode_frame(DECODED_FRAME)
        self.assertEqual(ENCODED_FRAME, encoded_frame)

    def test_encode_frame_recorded(self):
        """
        Tests encoding a KISS-encoded APRS.
        """
        encoded_frame = apex.aprs.Aprs._Aprs__encode_frame(DECODED_FRAME_RECORDED)
        self.assertEqual(ENCODED_FRAME_RECORDED, encoded_frame)

    def test_encode_frame_multipath(self):
        """
        Tests encoding a KISS-encoded APRS.
        """
        encoded_frame = apex.aprs.Aprs._Aprs__encode_frame(DECODED_FRAME_MULTIPATH)
        self.assertEqual(ENCODED_FRAME_MULTIPATH, encoded_frame)

    def test_decode_frame(self):
        """
        Tests KISS-encoding an APRS
        """
        decoded_frame = apex.aprs.Aprs._Aprs__decode_frame(ENCODED_FRAME)
        self.assertEqual(DECODED_FRAME, decoded_frame)

    def test_decode_frame_recorded(self):
        """
        Tests decoding a KISS-encoded APRS frame
        """
        decoded_frame = apex.aprs.Aprs._Aprs__decode_frame(ENCODED_FRAME_RECORDED)
        self.assertEqual(DECODED_FRAME_RECORDED, decoded_frame)

    def test_decode_frame_multipath(self):
        """
        Tests decoding a KISS-encoded APRS frame
        """
        decoded_frame = apex.aprs.Aprs._Aprs__decode_frame(ENCODED_FRAME_MULTIPATH)
        self.assertEqual(DECODED_FRAME_MULTIPATH, decoded_frame)

    def test_extract_path(self):
        """
        Tests extracting the APRS path from a KISS-encoded.
        """
        extracted_path = apex.aprs.Aprs._Aprs__extract_path(3, ENCODED_FRAME)
        self.assertEqual(DECODED_FRAME['path'][0], extracted_path[0])

    def test_idwentity_as_string_with_ssid(self):
        """
        Tests creating a full callsign string from a callsign+ssid dict using
        `aprs.util.full_callsign()`.
        """
        callsign = {
            'callsign': 'W2GMD',
            'ssid': 1
        }
        full_callsign = apex.aprs.Aprs._Aprs__identity_as_string(callsign)
        self.assertEqual(full_callsign, 'W2GMD-1')

    def test_identity_as_string_sans_ssid(self):
        """
        Tests creating a full callsign string from a callsign dict using
        `aprs.util.full_callsign()`.
        """
        callsign = {
            'callsign': 'W2GMD',
            'ssid': 0
        }
        full_callsign = apex.aprs.Aprs._Aprs__identity_as_string(callsign)
        self.assertEqual(full_callsign, 'W2GMD')

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
