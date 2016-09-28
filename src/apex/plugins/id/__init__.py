# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import click

import apex
import apex.aprs.util

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []
__version__ = '0.0.3'

plugin = None


def start(config, port_map, packet_cache, aprsis):
    global plugin
    plugin = IdPlugin(config, port_map, packet_cache, aprsis)
    plugin.run()


def handle_packet(frame, recv_port, recv_port_name):
    return


def stop():
    plugin.stop()


class IdPlugin(object):

    def __init__(self, config, port_map, packet_cache, aprsis):
        self.port_map = port_map
        self.packet_cache = packet_cache
        self.aprsis = aprsis
        self.running = False

        for section in config.sections():
            if section.startswith('TNC '):
                tnc_name = section.split(' ')[1]
                for port_id in range(1, 1+int(config.get(section, 'port_count'))):
                    port_name = tnc_name + '-' + str(port_id)
                    port = port_map[port_name]
                    port_section = 'PORT ' + port_name
                    port['id_text'] = config.get(port_section, 'id_text')
                    port['id_path'] = config.get(port_section, 'id_path')

    def stop(self):
        self.running = False

    def run(self):
        self.running = True

        # Don't do anything in the first 30 seconds
        last_trigger = time.time()
        while self.running and time.time() - last_trigger < 30:
            time.sleep(1)

        # run every 600 second
        last_trigger = time.time()
        while self.running:
            if time.time() - last_trigger >= 600:
                last_trigger = time.time()
                for port_name in self.port_map.keys():
                    port = self.port_map[port_name]

                    id_frame = {'source': port['identifier'], 'destination': 'ID', 'path': port['id_path'].split(','),
                                'text': port['id_text']}
                    frame_hash = apex.aprs.util.hash_frame(id_frame)
                    if frame_hash not in self.packet_cache.values():
                        self.packet_cache[str(frame_hash)] = frame_hash
                        port['tnc'].write(id_frame, port['tnc_port'])
                        apex.print_colorized_frame(id_frame, port_name, False)
            else:
                time.sleep(1)
