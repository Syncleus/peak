# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import click

import apex.aprs.util

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = "Jeffrey Phillips Freeman (WI2ARD)"
__email__ = "jeffrey.freeman@syncleus.com"
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

plugin = None


def start(config, port_map, packet_cache, aprsis):
    global plugin
    plugin = IdPlugin(config, port_map, packet_cache, aprsis)
    plugin.run()


def handle_packet(frame, recv_port, recv_port_name):
    return


class IdPlugin(object):

    def __init__(self, config, port_map, packet_cache, aprsis):
        self.port_map = port_map
        self.packet_cache = packet_cache
        self.aprsis = aprsis

        for section in config.sections():
            if section.startswith("TNC "):
                tnc_name = section.split(" ")[1]
                for port_id in range(1, 1+int(config.get(section, 'port_count'))):
                    port_name = tnc_name + '-' + str(port_id)
                    port = port_map[port_name]
                    port_section = 'PORT ' + port_name
                    port['id_text'] = config.get(port_section, 'id_text')
                    port['id_path'] = config.get(port_section, 'id_path')

    def run(self):
        time.sleep(30)
        while 1:
            for port_name in self.port_map.keys():
                port = self.port_map[port_name]

                id_frame = {'source': port['identifier'], 'destination': 'ID', 'path': port['id_path'].split(','),
                            'text': list(port['id_text'].encode('ascii'))}
                frame_hash = apex.aprs.util.hash_frame(id_frame)
                if frame_hash not in self.packet_cache.values():
                    self.packet_cache[str(frame_hash)] = frame_hash
                    port['tnc'].write(id_frame, port['tnc_port'])
                    click.echo(port_name + " >> " + apex.aprs.util.format_aprs_frame(id_frame))
            time.sleep(600)
