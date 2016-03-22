import importlib
import importlib.util
import importlib.machinery
import os

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