#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the entry point for the application, just a sandbox right now."""
import aprs.aprs_kiss

__author__ = 'Jeffrey Phillips Freeman WI2ARD <freemo@gmail.com>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'

import time
import signal
import sys
import kiss.constants
import aprs
import aprs.util
import threading

kenwood = aprs.AprsKiss(com_port="/dev/ttyUSB1", baud=9600)
kenwood.start(kiss.constants.MODE_INIT_KENWOOD_D710)
rpr = aprs.AprsKiss(com_port="/dev/ttyUSB0", baud=38400)
rpr.start(kiss.constants.MODE_INIT_W8DED)
aprsis = aprs.APRS('WI2ARD', '12345')

def sigint_handler(signal, frame):
    kenwood.close()
    rpr.close()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

print("Press ctrl + c at any time to exit")

#After 5 seconds send out a test package.
time.sleep(1)
beacon_frame_vhf = {
    'source': 'WI2ARD-1',
    'destination': 'APRS',
    'path': ['WIDE1-1', 'WIDE2-2'],
    'text': list(b'!/:=i@;N.G& --G/D R-I-R H24')
}

beacon_frame_hf = {
    'source': 'WI2ARD',
    'destination': 'APRS',
    'path': ['WIDE1-1'],
    'text': list(b'!/:=i@;N.G& --G/D R-I-R H24')
}

status_frame_vhf = {
    'source': 'WI2ARD-1',
    'destination': 'APRS',
    'path':['WIDE1-1', 'WIDE2-2'],
    'text': list(b'>Listening on 146.52Mhz http://JeffreyFreeman.me')
}

status_frame_hf = {
    'source': 'WI2ARD',
    'destination': 'APRS',
    'path': ['WIDE1-1'],
    'text': list(b'>Robust Packet Radio http://JeffreyFreeman.me')
}

#a = aprs.APRS('WI2ARD', '12345')
#a.connect("noam.aprs2.net".encode('ascii'), "14580".encode('ascii'))
#a.send('WI2ARD>APRS:>Hello World!')

def digipeat(frame, is_rpr):
    # can't digipeat things we already digipeated.
    for hop in frame['path']:
        if hop.startswith('WI2ARD') and hop.endswith('*'):
            return

    for hop_index in range(0,len(frame['path'])):
        hop = frame['path'][hop_index]
        if hop[-1] is not '*':
            split_hop = hop.split('-')
            node = split_hop[0].upper()

            if len(split_hop) >= 2 and split_hop[1]:
                ssid = int(split_hop[1])
            else:
                ssid = 0

            if node is 'WI2ARD' and ssid is 0:
                frame['path'][hop_index] = 'WI2ARD*'
                rpr.write(frame)
                print("R>> " + aprs.util.format_aprs_frame(frame))
                return
            elif node is 'WI2ARD' and ssid is 1:
                frame['path'][hop_index] = 'WI2ARD-1*'
                kenwood.write(frame)
                print("K>> " + aprs.util.format_aprs_frame(frame))
                return
            elif node.startswith('WIDE') and ssid > 1:
                if is_rpr:
                    frame['path'] = frame['path'][:hop_index-1] + ['WI2ARD*'] + [node + "-" + str(ssid-1)] + frame['path'][hop_index+1:]
                    rpr.write(frame)
                    print("R>> " + aprs.util.format_aprs_frame(frame))
                    return
                else:
                    frame['path'] = frame['path'][:hop_index-1] + ['WI2ARD-1*'] + [node + "-" + str(ssid-1)] + frame['path'][hop_index+1:]
                    kenwood.write(frame)
                    print("K>> " + aprs.util.format_aprs_frame(frame))
                    return
            elif node.startswith('WIDE') and ssid is 1:
                if is_rpr:
                    frame['path'] = frame['path'][:hop_index-1] + ['WI2ARD*'] + [node + "*"] + frame['path'][hop_index+1:]
                    rpr.write(frame)
                    print("R>> " + aprs.util.format_aprs_frame(frame))
                    return
                else:
                    frame['path'] = frame['path'][:hop_index-1] + ['WI2ARD-1*'] + [node + "*"] + frame['path'][hop_index+1:]
                    kenwood.write(frame)
                    print("K>> " + aprs.util.format_aprs_frame(frame))
                    return
            elif node.startswith('WIDE') and ssid is 0:
                frame['path'][hop_index] = node + "*"
                # no return


def kiss_reader_thread():
    print("Begining kiss reader thread...")
    while 1:
        something_read = False
        frame = kenwood.read()
        if frame is not None and len(frame):
            something_read = True
            digipeat(frame, False)
            formatted_aprs = aprs.util.format_aprs_frame(frame)
            print("K<< " + formatted_aprs)

        frame = rpr.read()
        if frame is not None and len(frame):
            something_read = True
            digipeat(frame, True)
            formatted_aprs = aprs.util.format_aprs_frame(frame)
            print("R<< " + formatted_aprs)

        if something_read is False:
            time.sleep(1)


threading.Thread(target=kiss_reader_thread, args=()).start()
while 1 :
    # let's wait one second before reading output (let's give device time to answer)
    kenwood.write(beacon_frame_vhf)
    print("K>> " + aprs.util.format_aprs_frame(beacon_frame_vhf))
    kenwood.write(status_frame_vhf)
    print("K>> " + aprs.util.format_aprs_frame(status_frame_vhf))

    rpr.write(beacon_frame_hf)
    print("R>> " + aprs.util.format_aprs_frame(beacon_frame_hf))
    rpr.write(status_frame_hf)
    print("R>> " + aprs.util.format_aprs_frame(status_frame_hf))
    time.sleep(600)

