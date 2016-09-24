#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KISS Core Classes."""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import serial

from apex.kiss import constants as kiss_constants

from .kiss import Kiss

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


class KissSerial(Kiss):

    """KISS Serial Object Class."""

    logger = logging.getLogger(__name__)
    logger.setLevel(kiss_constants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(kiss_constants.LOG_LEVEL)
    formatter = logging.Formatter(kiss_constants.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False

    frame_buffer = []

    def __init__(self, strip_df_start=True,
                 com_port=None,
                 baud=38400,
                 parity=serial.PARITY_NONE,
                 stop_bits=serial.STOPBITS_ONE,
                 byte_size=serial.EIGHTBITS):
        super(KissSerial, self).__init__(strip_df_start)

        self.com_port = com_port
        self.baud = baud
        self.parity = parity
        self.stop_bits = stop_bits
        self.byte_size = byte_size
        self.serial = None
        self.strip_df_start = strip_df_start
        self.exit_kiss = False

        self.logger.info('Using interface_mode=Serial')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serial.close()

    def __del__(self):
        if self.serial and self.serial.isOpen():
            self.serial.close()

    def _read_interface(self):
        read_data = self.serial.read(kiss_constants.READ_BYTES)
        waiting_data = self.serial.inWaiting()
        if waiting_data:
            read_data += self.serial.read(waiting_data)
        return map(ord, read_data)

    def _write_interface(self, data):
        self.serial.write(data)

    def start(self, mode_init=None, **kwargs):
        """
        Initializes the KISS device and commits configuration.

        See http://en.wikipedia.org/wiki/KISS_(TNC)#Command_codes
        for configuration names.

        :param **kwargs: name/value pairs to use as initial config values.
        """
        self.logger.debug('kwargs=%s', kwargs)

        self.serial = serial.Serial(port=self.com_port, baudrate=self.baud, parity=self.parity,
                                    stopbits=self.stop_bits, bytesize=self.byte_size)
        self.serial.timeout = kiss_constants.SERIAL_TIMEOUT
        if mode_init is not None:
            self.serial.write(mode_init)
            self.exit_kiss = True

        # Previous verious defaulted to Xastir-friendly configs. Unfortunately
        # those don't work with Bluetooth TNCs, so we're reverting to None.
        if kwargs:
            for name, value in kwargs.items():
                super(KissSerial, self).write_setting(name, value)

        # If no settings specified, default to config values similar
        # to those that ship with Xastir.
        # if not kwargs:
        #    kwargs = kiss.constants.DEFAULT_KISS_CONFIG_VALUES

    def close(self):
        super(KissSerial, self).close()

        if not self.serial:
            raise RuntimeError('Attempting to close before the class has been started.')
        elif self.serial.isOpen():
            self.serial.close()
