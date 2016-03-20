#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for the APRS Python Module."""

__author__ = 'Jeffrey Phillips Freeman WI2ARD <freemo@gmail.com>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'


import logging

import aprs.constants
import aprs.decimaldegrees
import kiss.constants
import math


def dec2dm_lat(dec):
    """Converts DecDeg to APRS Coord format.
    See: http://ember2ash.com/lat.htm

    Source: http://stackoverflow.com/questions/2056750

    Example:
        >>> test_lat = 37.7418096
        >>> aprs_lat = dec2dm_lat(test_lat)
        >>> aprs_lat
        '3744.51N'
    """
    dec_min = aprs.decimaldegrees.decimal2dm(dec)

    deg = dec_min[0]
    abs_deg = abs(deg)

    if not deg == abs_deg:
        suffix = 'S'
    else:
        suffix = 'N'

    return ''.join([str(abs_deg), "%.2f" % dec_min[1], suffix])


def dec2dm_lng(dec):
    """Converts DecDeg to APRS Coord format.
    See: http://ember2ash.com/lat.htm

    Example:
        >>> test_lng = -122.38833
        >>> aprs_lng = dec2dm_lng(test_lng)
        >>> aprs_lng
        '12223.30W'
    """
    dec_min = aprs.decimaldegrees.decimal2dm(dec)

    deg = dec_min[0]
    abs_deg = abs(deg)

    if not deg == abs_deg:
        suffix = 'W'
    else:
        suffix = 'E'

    return ''.join([str(abs_deg), "%.2f" % dec_min[1], suffix])


def decode_aprs_ascii_frame(ascii_frame):
    """
    Breaks an ASCII APRS Frame down to it's constituent parts.

    :param frame: ASCII APRS Frame.
    :type frame: str

    :returns: Dictionary of APRS Frame parts: source, destination, path, text.
    :rtype: dict
    """
    logging.debug('frame=%s', ascii_frame)
    decoded_frame = {}
    frame_so_far = ''

    for char in ascii_frame:
        if '>' in char and 'source' not in decoded_frame:
            decoded_frame['source'] = frame_so_far
            frame_so_far = ''
        elif ':' in char and 'path' not in decoded_frame:
            decoded_frame['path'] = frame_so_far
            frame_so_far = ''
        else:
            frame_so_far = ''.join([frame_so_far, char])

    decoded_frame['text'] = frame_so_far
    decoded_frame['destination'] = decoded_frame['path'].split(',')[0]

    return decoded_frame

def format_path(path_list):
    """
    Formats path from raw APRS KISS frame.

    :param path_list: List of path elements.
    :type path_list: list

    :return: Formatted APRS path.
    :rtype: str
    """
    return ','.join(path_list)


def format_aprs_frame(frame):
    """
    Formats APRS frame-as-dict into APRS frame-as-string.

    :param frame: APRS frame-as-dict
    :type frame: dict

    :return: APRS frame-as-string.
    :rtype: str
    """
    formatted_frame = '>'.join([frame['source'], frame['destination']])
    if frame['path']:
        formatted_frame = ','.join([formatted_frame, format_path(frame['path'])])
    formatted_frame += ':'
    for frame_byte in frame['text']:
        formatted_frame += chr(frame_byte)
    return formatted_frame


def valid_callsign(callsign):
    """
    Validates callsign.

    :param callsign: Callsign to validate.
    :type callsign: str

    :returns: True if valid, False otherwise.
    :rtype: bool
    """
    logging.debug('callsign=%s', callsign)

    if '-' in callsign:
        if not callsign.count('-') == 1:
            return False
        else:
            callsign, ssid = callsign.split('-')
    else:
        ssid = 0

    logging.debug('callsign=%s ssid=%s', callsign, ssid)

    if (len(callsign) < 2 or len(callsign) > 6 or len(str(ssid)) < 1 or
            len(str(ssid)) > 2):
        return False

    for char in callsign:
        if not (char.isalpha() or char.isdigit()):
            return False

    if not str(ssid).isdigit():
        return False

    if int(ssid) < 0 or int(ssid) > 15:
        return False

    return True


def run_doctest():  # pragma: no cover
    """Runs doctests for this module."""
    import doctest
    import aprs.util  # pylint: disable=W0406,W0621
    return doctest.testmod(aprs.util)


if __name__ == '__main__':
    run_doctest()  # pragma: no cover
