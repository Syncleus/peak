#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Util Module."""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import unittest

import apex.kiss
import apex.kiss.constants
import apex.kiss.util
from . import constants

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = "Jeffrey Phillips Freeman (WI2ARD)"
__email__ = "jeffrey.freeman@syncleus.com"
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


# pylint: disable=R0904,C0103
class KissUtilTestCase(unittest.TestCase):

    """Test class for KISS Python Module."""

    # All other tests only work on python2
    if sys.version_info < (3, 0):
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
            # fend = apex.kiss.util.escape_special_codes(apex.kiss.constants.FEND)
            fend = apex.kiss.Kiss._Kiss__escape_special_codes([apex.kiss.constants.FEND])  # pylint: disable=E1101
            self.assertEqual(fend, apex.kiss.constants.FESC_TFEND)

        def test_escape_special_codes_fesc(self):
            """
            Tests `kiss.util.escape_special_codes` util function.
            """
            fesc = apex.kiss.Kiss._Kiss__escape_special_codes([apex.kiss.constants.FESC])  # pylint: disable=E1101
            self.assertEqual(fesc, apex.kiss.constants.FESC_TFESC)



if __name__ == '__main__':
    unittest.main()
