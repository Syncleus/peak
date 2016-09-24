#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KISS Core Classes."""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import socket

from apex.kiss import constants as kissConstants
from .kiss import Kiss

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


class KissTcp(Kiss):

    """KISS TCP Object Class."""

    logger = logging.getLogger(__name__)
    logger.setLevel(kissConstants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(kissConstants.LOG_LEVEL)
    formatter = logging.Formatter(kissConstants.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False

    frame_buffer = []

    def __init__(self,
                 strip_df_start=True,
                 host=None,
                 tcp_port=8000):
        super(KissTcp, self).__init__(strip_df_start)

        self.host = host
        self.tcp_port = tcp_port
        self.socket = None
        self.strip_df_start = strip_df_start
        self.exit_kiss = False

        self.logger.info('Using interface_mode=TCP')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def _read_interface(self):
        return self.socket.recv(kissConstants.READ_BYTES)

    def _write_interface(self, data):
        self.socket.write(data)

    def start(self, mode_init=None, **kwargs):
        """
        Initializes the KISS device and commits configuration.

        See http://en.wikipedia.org/wiki/KISS_(TNC)#Command_codes
        for configuration names.

        :param **kwargs: name/value pairs to use as initial config values.
        """
        self.logger.debug('kwargs=%s', kwargs)

        address = (self.host, self.tcp_port)
        self.socket = socket.create_connection(address)

    def close(self):
        if not self.socket:
            raise RuntimeError('Attempting to close before the class has been started.')

        super(KissTcp, self).close()
        self.socket.shutdown()
        self.socket.close()

    def shutdown(self):
        self.socket.shutdown()
