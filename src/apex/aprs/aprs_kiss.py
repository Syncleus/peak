#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""APRS KISS Class Definitions"""

__author__ = 'Jeffrey Phillips Freeman WI2ARD <freemo@gmail.com>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'

import logging
import math

import apex.kiss


class AprsKiss(apex.kiss.Kiss):

    """APRS interface for KISS serial devices."""

    @staticmethod
    def __decode_frame(raw_frame):
        """
        Decodes a KISS-encoded APRS frame.

        :param raw_frame: KISS-encoded frame to decode.
        :type raw_frame: str

        :return: APRS frame-as-dict.
        :rtype: dict
        """
        logging.debug('raw_frame=%s', raw_frame)
        frame = {}
        frame_len = len(raw_frame)

        if frame_len > 16:
            for raw_slice in range(0, frame_len):
                # Is address field length correct?
                if raw_frame[raw_slice] & 0x01 and ((raw_slice + 1) % 7) == 0:
                    i = (raw_slice + 1) / 7
                    # Less than 2 callsigns?
                    if 1 < i < 11:
                        if (raw_frame[raw_slice + 1] & 0x03 == 0x03 and raw_frame[raw_slice + 2] in [0xf0, 0xcf]):
                            frame['text'] = raw_frame[raw_slice + 3:]
                            frame['destination'] = AprsKiss.__identity_as_string(AprsKiss.__extract_callsign(raw_frame))
                            frame['source'] = AprsKiss.__identity_as_string(AprsKiss.__extract_callsign(raw_frame[7:]))
                            frame['path'] = AprsKiss.__extract_path(math.floor(i), raw_frame)
                            return frame

        logging.debug('frame=%s', frame)
        return frame

    @staticmethod
    def __extract_path(start, raw_frame):
        """Extracts path from raw APRS KISS frame.

        :param start:
        :param raw_frame: Raw APRS frame from a KISS device.

        :return: Full path from APRS frame.
        :rtype: list
        """
        full_path = []

        for i in range(2, start):
            path = AprsKiss.__identity_as_string(AprsKiss.__extract_callsign(raw_frame[i * 7:]))
            if path:
                if raw_frame[i * 7 + 6] & 0x80:
                    full_path.append(''.join([path, '*']))
                else:
                    full_path.append(path)

        return full_path

    @staticmethod
    def __extract_callsign(raw_frame):
        """
        Extracts callsign from a raw KISS frame.

        :param raw_frame: Raw KISS Frame to decode.
        :returns: Dict of callsign and ssid.
        :rtype: dict
        """
        callsign = ''.join([chr(x >> 1) for x in raw_frame[:6]]).strip()
        ssid = ((raw_frame[6]) >> 1) & 0x0f
        return {'callsign': callsign, 'ssid': ssid}

    @staticmethod
    def __identity_as_string(identity):
        """
        Returns a fully-formatted callsign (Callsign + SSID).

        :param identity: Callsign Dictionary {'callsign': '', 'ssid': n}
        :type callsign: dict
        :returns: Callsign[-SSID].
        :rtype: str
        """
        if identity['ssid'] > 0:
            return '-'.join([identity['callsign'], str(identity['ssid'])])
        else:
            return identity['callsign']

    @staticmethod
    def __encode_frame(frame):
        """
        Encodes an APRS frame-as-dict as a KISS frame.

        :param frame: APRS frame-as-dict to encode.
        :type frame: dict

        :return: KISS-encoded APRS frame.
        :rtype: list
        """
        enc_frame = AprsKiss.__encode_callsign(AprsKiss.__parse_identity_string(frame['destination'])) + AprsKiss.__encode_callsign(AprsKiss.__parse_identity_string(frame['source']))
        for p in frame['path']:
            enc_frame += AprsKiss.__encode_callsign(AprsKiss.__parse_identity_string(p))

        return enc_frame[:-1] + [enc_frame[-1] | 0x01] + [apex.kiss.constants.SLOT_TIME] + [0xf0] + frame['text']

    @staticmethod
    def __encode_callsign(callsign):
        """
        Encodes a callsign-dict within a KISS frame.

        :param callsign: Callsign-dict to encode.
        :type callsign: dict

        :return: KISS-encoded callsign.
        :rtype: list
        """
        call_sign = callsign['callsign']

        enc_ssid = (callsign['ssid'] << 1) | 0x60

        if '*' in call_sign:
            call_sign = call_sign.replace('*', '')
            enc_ssid |= 0x80

        while len(call_sign) < 6:
            call_sign = ''.join([call_sign, ' '])

        encoded = []
        for p in call_sign:
            encoded += [ord(p) << 1]
        return encoded + [enc_ssid]

    @staticmethod
    def __parse_identity_string(identity_string):
        """
        Creates callsign-as-dict from callsign-as-string.

        :param identity_string: Callsign-as-string (with or without ssid).
        :type raw_callsign: str

        :return: Callsign-as-dict.
        :rtype: dict
        """
        # If we are parsing a spent token then first lets get rid of the astresick suffix.
        if identity_string.endswith('*'):
            identity_string = identity_string[:-1]

        if '-' in identity_string:
            call_sign, ssid = identity_string.split('-')
        else:
            call_sign = identity_string
            ssid = 0
        return {'callsign': call_sign, 'ssid': int(ssid)}

    def write(self, frame, port=0):
        """Writes APRS-encoded frame to KISS device.

        :param frame: APRS frame to write to KISS device.
        :type frame: dict
        """
        encoded_frame = AprsKiss.__encode_frame(frame)
        super(AprsKiss, self).write(encoded_frame, port)

    def read(self):
        """Reads APRS-encoded frame from KISS device.
        """
        frame = super(AprsKiss, self).read()
        if frame is not None and len(frame):
            return AprsKiss.__decode_frame(frame)
        else:
            return None
