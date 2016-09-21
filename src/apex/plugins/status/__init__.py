# These imports are for python3 compatability inside python2
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import apex.aprs.util
import time

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = "Jeffrey Phillips Freeman (WI2ARD)"
__email__ = "jeffrey.freeman@syncleus.com"
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

plugin = None


def start(config, port_map, packet_cache, aprsis):
    global plugin
    plugin = StatusPlugin(config, port_map, packet_cache, aprsis)
    plugin.run()


def handle_packet(frame, recv_port, recv_port_name):
    return


class StatusPlugin(object):

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
                    port['status_text'] = config.get(port_section, 'status_text')
                    port['status_path'] = config.get(port_section, 'status_path')

    def run(self):
        time.sleep(60)
        while 1:
            for port_name in self.port_map.keys():
                port = self.port_map[port_name]

                status_frame = {
                    'source': port['identifier'],
                    'destination': 'APRS',
                    'path': port['status_path'].split(','),
                    'text': list(port['status_text'].encode('ascii'))}
                frame_hash = apex.aprs.util.hash_frame(status_frame)
                if frame_hash not in self.packet_cache.values():
                    self.packet_cache[str(frame_hash)] = frame_hash
                    port['tnc'].write(status_frame, port['tnc_port'])
                    print(port_name + " >> " + apex.aprs.util.format_aprs_frame(status_frame))
            time.sleep(600)
