#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Util Module."""

__author__ = 'Jeffrey Phillips Freeman WI2ARD <freemo@gmail.com>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'


import unittest

from . import constants

import apex
import apex.kiss.constants
import apex.kiss.util


# pylint: disable=R0904,C0103
class KISSUtilTestCase(unittest.TestCase):

    """Test class for KISS Python Module."""

    def setUp(self):
        """Setup."""
        self.test_frames = open(constants.TEST_FRAMES, 'r')
        self.test_frame = self.test_frames.readlines()[0].strip()

    def tearDown(self):
        """Teardown."""
        self.test_frames.close()

    def test_escape_special_codes_fend(self):
        """
        Tests `kiss.util.escape_special_codes` util function.
        """
        fend = apex.kiss.util.escape_special_codes(apex.kiss.constants.FEND)
        self.assertEqual(fend, apex.kiss.constants.FESC_TFEND)

    def test_escape_special_codes_fesc(self):
        """
        Tests `kiss.util.escape_special_codes` util function.
        """
        fesc = apex.kiss.util.escape_special_codes(apex.kiss.constants.FESC)
        self.assertEqual(fesc, apex.kiss.constants.FESC_TFESC)

    def test_extract_ui(self):
        """
        Tests `kiss.util.extract_ui` util function.
        """
        frame_ui = apex.kiss.util.extract_ui(self.test_frame)
        self.assertEqual('APRX240W2GMD 6WIDE1 1', frame_ui)


if __name__ == '__main__':
    unittest.main()
