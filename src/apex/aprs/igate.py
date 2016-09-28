#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""APRS Internet Service Class Definitions"""

# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import select
import socket
import threading
import time
import cachetools
import requests

from apex.aprs import constants as aprs_constants
from apex.aprs import util as aprs_util

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []


class ReconnectingPacketBuffer(object):

    STARTING_WAIT_TIME = 2
    MAX_WAIT_TIME = 300
    WAIT_TIME_MULTIPLIER = 2
    MAX_INDEX = 1000000

    def __init__(self, packet_layer):
        self.packet_layer = packet_layer
        self.to_packet_layer = cachetools.TTLCache(10, 30)
        self.current_index = 0
        self.from_packet_layer = cachetools.TTLCache(10, 30)
        self.connect_thread = None
        self.lock = threading.Lock()
        self.running = False
        self.reconnect_wait_time = self.STARTING_WAIT_TIME
        self.last_connect_attempt = None
        self.connect_args = None
        self.connect_kwargs = None
        self.connected = False

    def __increment_wait_time(self):
        self.reconnect_wait_time *= self.WAIT_TIME_MULTIPLIER
        if self.reconnect_wait_time > self.MAX_WAIT_TIME:
            self.reconnect_wait_time = self.MAX_WAIT_TIME

    def __reset_wait_time(self):
        self.reconnect_wait_time = self.STARTING_WAIT_TIME

    def __run(self):
        while self.running:
            if not self.connected:
                if not self.last_connect_attempt or time.time() - self.last_connect_attempt > self.reconnect_wait_time:
                    try:
                        self.last_connect_attempt = time.time()
                        self.packet_layer.connect(*self.connect_args, **self.connect_kwargs)
                        self.connected = True
                    except IOError:
                        try:
                            self.packet_layer.close()
                        except IOError:
                            pass
                        self.__increment_wait_time()
                else:
                    time.sleep(1)
            else:
                io_occured = False

                # lets attempt to read in a packet
                try:
                    read_packet = self.packet_layer.read()
                    self.__reset_wait_time()
                    if read_packet:
                        with self.lock:
                                self.from_packet_layer[str(aprs_util.hash_frame(read_packet))] = read_packet
                        io_occured = True
                except IOError:
                    try:
                        self.packet_layer.close()
                    except IOError:
                        pass
                    self.connected = False
                    continue

                # lets try to write a packet, if any are waiting.
                write_packet = None
                with self.lock:
                    if self.to_packet_layer:
                        write_packet = self.to_packet_layer.popitem()[1]
                if write_packet:
                    try:
                        self.packet_layer.write(write_packet)
                        io_occured = True
                        self.__reset_wait_time()
                    except IOError:
                        self.to_packet_layer[str(aprs_util.hash_frame(read_packet))] = write_packet
                        try:
                            self.packet_layer.close()
                        except IOError:
                            pass
                        self.connected = False
                        continue

                if not io_occured:
                    time.sleep(1)
        try:
            self.packet_layer.close()
        except IOError:
            pass

    def connect(self, *args, **kwargs):
        with self.lock:
            if self.connect_thread:
                raise RuntimeError('already connected')

            self.running = True
            self.connect_args = args
            self.connect_kwargs = kwargs
            self.connect_thread = threading.Thread(target=self.__run)
            self.connect_thread.start()

    def close(self):
        with self.lock:
            if not self.connect_thread:
                raise RuntimeError('not connected')

            self.running = False
            self.connect_thread.join()
            self.connect_thread = None

    def read(self):
        with self.lock:
            if self.from_packet_layer:
                return self.from_packet_layer.popitem()[1]
        return None

    def write(self, packet):
        with self.lock:
            self.to_packet_layer[str(aprs_util.hash_frame(read_packet))] = packet


class IGate(object):

    """APRS Object."""

    logger = logging.getLogger(__name__)
    logger.setLevel(aprs_constants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(aprs_constants.LOG_LEVEL)
    console_handler.setFormatter(aprs_constants.LOG_FORMAT)
    logger.addHandler(console_handler)
    logger.propagate = False

    def __init__(self, user, password='-1', input_url=None):
        self.user = user
        self._url = input_url or aprs_constants.APRSIS_URL
        self._auth = ' '.join(
            ['user', user, 'pass', password, 'vers', 'APRS Python Module'])
        self.aprsis_sock = None
        self.data_buffer = ''
        self.packet_buffer = []

    def __reset_buffer(self):
        self.data_buffer = ''
        self.packet_buffer = []

    def connect(self, server=None, port=None, aprs_filter=None):
        """
        Connects & logs in to APRS-IS.

        :param server: Optional alternative APRS-IS server.
        :param port: Optional APRS-IS port.
        :param filter: Optional filter to use.
        :type server: str
        :type port: int
        :type filte: str
        """
        if not self.aprsis_sock:
            self.__reset_buffer()

            server = server or aprs_constants.APRSIS_SERVER
            port = port or aprs_constants.APRSIS_FILTER_PORT
            aprs_filter = aprs_filter or '/'.join(['p', self.user])

            self.full_auth = ' '.join([self._auth, 'filter', aprs_filter])

            self.server = server
            self.port = port
            self.aprsis_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.aprsis_sock.connect((server, port))
            self.logger.info('Connected to server=%s port=%s', server, port)
            self.logger.debug('Sending full_auth=%s', self.full_auth)
            self.aprsis_sock.sendall((self.full_auth + '\n\r').encode('ascii'))

    def close(self):
        if self.aprsis_sock:
            self.aprsis_sock.close()
            self.__reset_buffer()
            self.aprsis_sock = None

    def write(self, frame_decoded, headers=None, protocol='TCP'):
        """
        Sends message to APRS-IS.

        :param message: Message to send to APRS-IS.
        :param headers: Optional HTTP headers to post.
        :param protocol: Protocol to use: One of TCP, HTTP or UDP.
        :type message: str
        :type headers: dict

        :return: True on success, False otherwise.
        :rtype: bool
        """

        frame = aprs_util.encode_frame(frame_decoded)
        if 'TCP' in protocol:
            self.aprsis_sock.sendall(frame)
            return True
        elif 'HTTP' in protocol:
            content = '\n'.join([self._auth, frame])
            headers = headers or aprs_constants.APRSIS_HTTP_HEADERS
            result = requests.post(self._url, data=content, headers=headers)
            return 204 == result.status_code
        elif 'UDP' in protocol:
            content = '\n'.join([self._auth, frame])
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(
                content,
                (aprs_constants.APRSIS_SERVER, aprs_constants.APRSIS_RX_PORT)
            )
            return True

    def read(self, filter_logresp=True):
        """
        Receives from APRS-IS.

        :param callback: Optional callback to deliver data to.
        :type callback: func
        """
        # check if there is any data waiting
        read_more = True
        while read_more:
            selected = select.select([self.aprsis_sock], [], [], 0)
            if len(selected[0]) > 0:
                recvd_data = self.aprsis_sock.recv(aprs_constants.RECV_BUFFER)
                if not recvd_data:
                    self.data_buffer += recvd_data
                else:
                    read_more = False
            else:
                read_more = False

        # check for any complete packets and move them to the packet buffer
        if '\r\n' in self.data_buffer:
            partial = True
            if self.data_buffer.endswith('\r\n'):
                partial = False
            packets = recvd_data.split('\r\n')
            if partial:
                self.data_buffer = str(packets.pop(-1))
            else:
                self.data_buffer = ''
            for packet in packets:
                self.packet_buffer += [str(packet)]

        # return the next packet that matches the filter
        while len(self.packet_buffer):
            packet = self.packet_buffer.pop(0)
            if filter_logresp and packet.startswith('#') and 'logresp' in packet:
                pass
            else:
                return aprs_util.decode_frame(packet)

        return None
