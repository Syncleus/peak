"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mapex` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``apex.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``apex.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
# These imports are for python3 compatability inside python2
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import sys
import click
import time
import signal
import sys
import threading
import cachetools
import traceback
from apex.pluginloader import getPlugins, loadPlugin

if sys.version_info < (3, 0):
    import ConfigParser
elif sys.version_info >= (3, 0):
    import configparser

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = "Jeffrey Phillips Freeman (WI2ARD)"
__email__ = "jeffrey.freeman@syncleus.com"
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

from apex.kiss import constants as kissConstants
import apex.aprs


@click.command()
@click.argument('names', nargs=-1)
def main(names):
    click.echo(repr(names))

    port_map = {}
    config = configparser.ConfigParser()
    config.read('apex.cfg')
    for section in config.sections():
        if section.startswith("TNC "):
            tnc_name = section.split(" ")[1]
            if config.has_option(section, 'com_port') and config.has_option(section, 'baud'):
                com_port = config.get(section, 'com_port')
                baud = config.get(section, 'baud')
                kiss_tnc = apex.aprs.AprsKiss(com_port=com_port, baud=baud)
            elif config.has_option(section, 'tcp_host') and config.has_option(section, 'tcp_port'):
                tcp_host = config.get(section, 'tcp_host')
                tcp_port = config.get(section, 'tcp_port')
                kiss_tnc = apex.aprs.AprsKiss(host=tcp_host, tcp_port=tcp_port)
            else:
                raise Exception(
                    "Must have either both com_port and baud set or tcp_host and tcp_port set in configuration file")
            kiss_init_string = config.get(section, 'kiss_init')
            if kiss_init_string == 'MODE_INIT_W8DED':
                kiss_tnc.start(kissConstants.MODE_INIT_W8DED)
            elif kiss_init_string == 'MODE_INIT_KENWOOD_D710':
                kiss_tnc.start(kissConstants.MODE_INIT_KENWOOD_D710)
            elif kiss_init_string == 'NONE':
                kiss_tnc.start()
            else:
                raise Exception("KISS init mode not specified")
            for port in range(1, 1 + int(config.get(section, 'port_count'))):
                port_name = tnc_name + '-' + str(port)
                port_section = 'PORT ' + port_name
                port_identifier = config.get(port_section, 'identifier')
                port_net = config.get(port_section, 'net')
                tnc_port = int(config.get(port_section, 'tnc_port'))
                port_map[port_name] = {'identifier': port_identifier, 'net': port_net, 'tnc': kiss_tnc,
                                       'tnc_port': tnc_port}
    aprsis_callsign = config.get('APRS-IS', 'callsign')
    if config.has_option('APRS-IS', 'password'):
        aprsis_password = config.get('APRS-IS', 'password')
    else:
        aprsis_password = -1
    aprsis_server = config.get('APRS-IS', 'server')
    aprsis_server_port = config.get('APRS-IS', 'server_port')
    aprsis = apex.aprs.AprsInternetService(aprsis_callsign, aprsis_password)
    aprsis.connect(aprsis_server, int(aprsis_server_port))
    packet_cache = cachetools.TTLCache(10000, 5)

    def sigint_handler(signal, frame):
        for port in port_map.values():
            port['tnc'].close()
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    print("Press ctrl + c at any time to exit")

    # start the plugins
    plugins = []
    plugin_loaders = getPlugins()
    for plugin_loader in plugin_loaders:
        loaded_plugin = loadPlugin(plugin_loader)
        plugins.append(loaded_plugin)
        threading.Thread(target=loaded_plugin.start, args=(config, port_map, packet_cache, aprsis)).start()

    while 1:
        something_read = False
        try:
            for port_name in port_map.keys():
                port = port_map[port_name]
                frame = port['tnc'].read()
                if frame:
                    formatted_aprs = apex.aprs.util.format_aprs_frame(frame)
                    print(port_name + " << " + formatted_aprs)
                    for plugin in plugins:
                        something_read = True
                        plugin.handle_packet(frame, port, port_name)
        except Exception as ex:
            # We want to keep this thread alive so long as the application runs.
            traceback.print_exc(file=sys.stdout)
            print("caught exception while reading packet: " + str(ex))

        if something_read is False:
            time.sleep(1)
