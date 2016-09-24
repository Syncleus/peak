#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for the KISS Python Module."""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import apex.kiss.constants

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


def extract_ui(frame):
    """
    Extracts the UI component of an individual frame.

    :param frame: APRS/AX.25 frame.
    :type frame: str
    :returns: UI component of frame.
    :rtype: str
    """
    start_ui = frame.split(
        ''.join([apex.kiss.constants.FEND, apex.kiss.constants.DATA_FRAME]))
    end_ui = start_ui[0].split(''.join([apex.kiss.constants.SLOT_TIME, chr(0xF0)]))
    return ''.join([chr(ord(x) >> 1) for x in end_ui[0]])
