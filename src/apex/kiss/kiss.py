#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KISS Core Classes."""

# These imports are for python3 compatability inside python2
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import logging
import serial
import socket
from apex.kiss import constants as kissConstants

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = "Jeffrey Phillips Freeman (WI2ARD)"
__email__ = "jeffrey.freeman@syncleus.com"
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


class Kiss(object):

    """KISS Object Class."""

    logger = logging.getLogger(__name__)
    logger.setLevel(kissConstants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(kissConstants.LOG_LEVEL)
    formatter = logging.Formatter(kissConstants.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False

    frame_buffer = []

    def __init__(self, com_port=None,
                 baud=38400,
                 parity=serial.PARITY_NONE,
                 stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS,
                 host=None,
                 tcp_port=8000,
                 strip_df_start=True):
        self.com_port = com_port
        self.baud = baud
        self.parity = parity
        self.stop_bits = stop_bits
        self.byte_size = byte_size
        self.host = host
        self.tcp_port = tcp_port
        self.interface = None
        self.interface_mode = None
        self.strip_df_start = strip_df_start
        self.exit_kiss = False

        if self.com_port is not None:
            self.interface_mode = 'serial'
        elif self.host is not None:
            self.interface_mode = 'tcp'
        if self.interface_mode is None:
            raise Exception('Must set port/speed or host/tcp_port.')

        self.logger.info('Using interface_mode=%s', self.interface_mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if 'tcp' in self.interface_mode:
            self.interface.shutdown()
        elif self.interface and self.interface.isOpen():
            self.interface.close()

    def __del__(self):
        if self.interface and self.interface.isOpen():
            self.interface.close()

    def __read_interface(self):
        if 'tcp' in self.interface_mode:
            return self.interface.recv(kissConstants.READ_BYTES)
        elif 'serial' in self.interface_mode:
            read_data = self.interface.read(kissConstants.READ_BYTES)
            waiting_data = self.interface.inWaiting()
            if waiting_data:
                read_data += self.interface.read(waiting_data)
            return read_data

    @staticmethod
    def __strip_df_start(frame):
        """
        Strips KISS DATA_FRAME start (0x00) and newline from frame.

        :param frame: APRS/AX.25 frame.
        :type frame: str
        :returns: APRS/AX.25 frame sans DATA_FRAME start (0x00).
        :rtype: str
        """
        while frame[0] is kissConstants.DATA_FRAME:
            del frame[0]
        while chr(frame[0]).isspace():
            del frame[0]
        while chr(frame[-1]).isspace():
            del frame[-1]
        return frame

    @staticmethod
    def __escape_special_codes(raw_code_bytes):
        """
        Escape special codes, per KISS spec.

        "If the FEND or FESC codes appear in the data to be transferred, they
        need to be escaped. The FEND code is then sent as FESC, TFEND and the
        FESC is then sent as FESC, TFESC."
        - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
        """
        encoded_bytes = []
        for raw_code_byte in raw_code_bytes:
            if raw_code_byte is kissConstants.FESC:
                encoded_bytes += kissConstants.FESC_TFESC
            elif raw_code_byte is kissConstants.FEND:
                encoded_bytes += kissConstants.FESC_TFEND
            else:
                encoded_bytes += [raw_code_byte]
        return encoded_bytes

    @staticmethod
    def __command_byte_combine(port, command_code):
        """
        Constructs the command byte for the tnc which includes the tnc port and command code.
        :param port: integer from 0 to 127 indicating the TNC port
        :type port: int
        :param command_code: A command code constant, a value from 0 to 127
        :type command_code: int
        :return: An integer combining the two values into a single byte
        """
        if port > 127 or port < 0:
            raise Exception("port out of range")
        elif command_code > 127 or command_code < 0:
            raise Exception("command_Code out of range")
        return (port << 4) & command_code

    def start(self, mode_init=None, **kwargs):
        """
        Initializes the KISS device and commits configuration.

        See http://en.wikipedia.org/wiki/KISS_(TNC)#Command_codes
        for configuration names.

        :param **kwargs: name/value pairs to use as initial config values.
        """
        self.logger.debug("kwargs=%s", kwargs)

        if 'tcp' in self.interface_mode:
            address = (self.host, self.tcp_port)
            self.interface = socket.create_connection(address)
        elif 'serial' in self.interface_mode:
            self.interface = serial.Serial(port=self.com_port, baudrate=self.baud, parity=self.parity,
                                           stopbits=self.stop_bits, bytesize=self.byte_size)
            self.interface.timeout = kissConstants.SERIAL_TIMEOUT
            if mode_init is not None:
                self.interface.write(mode_init)
                self.exit_kiss = True

        # Previous verious defaulted to Xastir-friendly configs. Unfortunately
        # those don't work with Bluetooth TNCs, so we're reverting to None.
        if 'serial' in self.interface_mode and kwargs:
            for name, value in kwargs.items():
                self.write_setting(name, value)

        # If no settings specified, default to config values similar
        # to those that ship with Xastir.
        # if not kwargs:
        #    kwargs = kiss.constants.DEFAULT_KISS_CONFIG_VALUES

    def close(self):
        if self.exit_kiss is True:
            self.interface.write(kissConstants.MODE_END)

    def write_setting(self, name, value):
        """
        Writes KISS Command Codes to attached device.

        http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes

        :param name: KISS Command Code Name as a string.
        :param value: KISS Command Code Value to write.
        """
        self.logger.debug('Configuring %s = %s', name, repr(value))

        # Do the reasonable thing if a user passes an int
        if isinstance(value, int):
            value = chr(value)

        return self.interface.write(
            kissConstants.FEND +
            getattr(kissConstants, name.upper()) +
            Kiss.__escape_special_codes(value) +
            kissConstants.FEND
        )

    def fill_buffer(self):
        """
        Reads any pending data in the interface and stores it in the frame_buffer
        """

        new_frames = []
        read_buffer = []
        read_data = self.__read_interface()
        while read_data is not None and len(read_data):
            split_data = [[]]
            for read_byte in read_data:
                if read_byte is kissConstants.FEND:
                    split_data.append([])
                else:
                    split_data[-1].append(read_byte)
            len_fend = len(split_data)

            # No FEND in frame
            if len_fend == 1:
                read_buffer += split_data[0]
            # Single FEND in frame
            elif len_fend == 2:
                # Closing FEND found
                if split_data[0]:
                    # Partial frame continued, otherwise drop
                    new_frames.append(read_buffer + split_data[0])
                    read_buffer = []
                # Opening FEND found
                else:
                    new_frames.append(read_buffer)
                    read_buffer = split_data[1]
            # At least one complete frame received
            elif len_fend >= 3:
                for i in range(0, len_fend - 1):
                    read_buffer_tmp = read_buffer + split_data[i]
                    if len(read_buffer_tmp) is not 0:
                        new_frames.append(read_buffer_tmp)
                        read_buffer = []
                if split_data[len_fend - 1]:
                    read_buffer = split_data[len_fend - 1]
            # Get anymore data that is waiting
            read_data = self.__read_interface()

        for new_frame in new_frames:
            if len(new_frame) and new_frame[0] == 0:
                if self.strip_df_start:
                    new_frame = Kiss.__strip_df_start(new_frame)
                self.frame_buffer.append(new_frame)

    def read(self):
        if not len(self.frame_buffer):
            self.fill_buffer()

        if len(self.frame_buffer):
            return_frame = self.frame_buffer[0]
            del self.frame_buffer[0]
            return return_frame
        else:
            return None

    def write(self, frame_bytes, port=0):
        """
        Writes frame to KISS interface.

        :param frame: Frame to write.
        """
        kiss_packet = [kissConstants.FEND] + [Kiss.__command_byte_combine(port, kissConstants.DATA_FRAME)] +\
            Kiss.__escape_special_codes(frame_bytes) + [kissConstants.FEND]

        if 'tcp' in self.interface_mode:
            return self.interface.send(bytearray(kiss_packet))
        elif 'serial' in self.interface_mode:
            return self.interface.write(kiss_packet)
