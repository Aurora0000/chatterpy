#!/usr/bin/env python
from yapsy.PluginManager import PluginManagerSingleton
import json
import os
import os.path

class PluginConfigurationManager:
    configs = {}
    def __init__(self, folder):
        self.folder = folder
        self.collect_settings()
    
    def collect_settings(self):
        for dirpath, dirnames, filenames in os.walk(self.folder):
            for fn in [f for f in filenames if f.endswith(".chatterconf")]:
                self.configs[(fn.split(".")[0])] = os.path.join(dirpath, fn)
    def get_setting(self, setting, domain):
        # No error checking, if there's a problem, the caller needs to catch it
        f = open(self.configs[domain])
        json_data = json.loads(f.read())
        f.close()
        return json_data[setting]
    def set_setting(self, setting, domain, value):
        f = open(self.configs[domain], "r+")
        json_data = json.loads(f.read())
        json_data[setting] = value
        f.seek(0) 
        f.write(json.dumps(json_data, indent=4))
        f.truncate()
        f.close()
    def get_json_data(self, domain):
        f = open(self.configs[domain])
        json_data = json.loads(f.read())
        f.close()
        return json_data
