#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Util Module."""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
# import apex.kiss.util

from . import constants

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


# pylint: disable=R0904,C0103
class KissUtilTestCase(unittest.TestCase):

    """Test class for KISS Python Module."""

    def setUp(self):
        """Setup."""
        self.test_frames = open(constants.TEST_FRAMES, 'r')
        self.test_frame = self.test_frames.readlines()[0].strip()

    def tearDown(self):
        """Teardown."""
        self.test_frames.close()

    # # All other tests only work on python2
    # def test_extract_ui(self):
    #     """
    #     Tests `kiss.util.extract_ui` util function.
    #     """
    #     frame_ui = apex.kiss.util.extract_ui(self.test_frame)
    #     self.assertEqual('APRX240W2GMD 6WIDE1 1', frame_ui)


if __name__ == '__main__':
    unittest.main()
