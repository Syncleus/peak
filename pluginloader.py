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
        info = importlib.util._find_spec_from_path(MainModule, [location])
        plugins.append({"name": i, "spec": info})
    return plugins

def loadPlugin(plugin):
    return plugin['spec'].loader.load_module()