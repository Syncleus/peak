# These imports are for python3 compatability inside python2
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import importlib
import os

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = "Jeffrey Phillips Freeman (WI2ARD)"
__email__ = "jeffrey.freeman@syncleus.com"
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

PluginFolder = "./plugins"
MainModule = "__init__"


def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue

        plugins.append(i)
    return plugins


def loadPlugin(plugin):
    return importlib.import_module("plugins." + plugin)
