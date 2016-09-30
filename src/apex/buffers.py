#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading
import time

import cachetools

from apex.aprs import util as aprs_util
from .util import echo_colorized_frame
from .util import echo_colorized_warning


class NonrepeatingBuffer(object):
    def __init__(self, base_tnc, base_name, base_port=None, echo_packets=True, buffer_size=10000, buffer_time=30):
        self.packet_cache = cachetools.TTLCache(buffer_size, buffer_time)
        self.lock = threading.Lock()
        self.base_tnc = base_tnc
        self.base_port = base_port
        self.base_name = base_name
        self.echo_packets = echo_packets

    @property
    def port(self):
        return self.base_port

    @property
    def name(self):
        return self.base_name

    def connect(self, *args, **kwargs):
        self.base_tnc.connect(*args, **kwargs)

    def close(self, *args, **kwargs):
        self.base_tnc.close(*args, **kwargs)

    def write(self, frame, *args, **kwargs):
        with self.lock:
            frame_hash = str(aprs_util.hash_frame(frame))
            if frame_hash not in self.packet_cache:
                self.packet_cache[frame_hash] = frame
                if self.base_port:
                    self.base_tnc.write(frame, self.base_port)
                else:
                    self.base_tnc.write(frame)

                if self.echo_packets:
                    echo_colorized_frame(frame, self.base_name, False)

    def read(self, *args, **kwargs):
        with self.lock:
            frame = self.base_tnc.read(*args, **kwargs)
            if not frame:
                return frame
            frame_hash = str(aprs_util.hash_frame(frame))
            if frame_hash not in self.packet_cache:
                self.packet_cache[frame_hash] = frame
                if self.echo_packets:
                    echo_colorized_frame(frame, self.base_name, True)
                return frame
            else:
                return None


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
                        echo_colorized_warning('Could not connect, will reattempt.')
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
                    echo_colorized_warning('Read failed. Will disconnect and attempt to reconnect.')
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
                        echo_colorized_warning('Write failed. Will disconnect and attempt to reconnect.')
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
            self.to_packet_layer[str(aprs_util.hash_frame(packet))] = packet
