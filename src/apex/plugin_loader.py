# These imports are for python3 compatability inside python2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import os

__author__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__maintainer__ = 'Jeffrey Phillips Freeman (WI2ARD)'
__email__ = 'jeffrey.freeman@syncleus.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016, Syncleus, Inc. and contributors'
__credits__ = []

PluginFolder = './plugins'
MainModule = '__init__'

plugins = ['plugins.apexparadigm',
           'plugins.beacon',
           'plugins.id',
           'plugins.status']


def get_plugins():
    return plugins


def load_plugin(plugin):
    return importlib.import_module(plugin)
