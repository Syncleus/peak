#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for the KISS Python Module."""

__author__ = 'Jeffrey Phillips Freeman WI2ARD <freemo@gmail.com>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'


import apex.kiss.constants

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


