#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These imports are for python3 compatibility inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading
import cachetools

import apex.aprs.util


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
            frame_hash = str(apex.aprs.util.hash_frame(frame))
            if frame_hash not in self.packet_cache:
                self.packet_cache[frame_hash] = frame
                if self.base_port:
                    self.base_tnc.write(frame, self.base_port)
                else:
                    self.base_tnc.write(frame)

                if self.echo_packets:
                    apex.echo_colorized_frame(frame, self.base_name, False)

    def read(self, *args, **kwargs):
        with self.lock:
            frame = self.base_tnc.read(*args, **kwargs)
            if not frame:
                return frame
            frame_hash = str(apex.aprs.util.hash_frame(frame))
            if frame_hash not in self.packet_cache:
                self.packet_cache[frame_hash] = frame
                if self.echo_packets:
                    apex.echo_colorized_frame(frame, self.base_name, True)
                return frame
            else:
                return None
