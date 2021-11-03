"""
tto_globals - program globals for tto

This module handles program-wide globals, other variables, data, machine
states, etc for tto.


Requirements
------------
configparser : to read machine-specific config file containing program options.
tto_debugger : logging module for tto

Classes
-------
TtoGlobals : handles instrument configuration files and options.

Variables
---------
tto_globals : global instance of TtoGlobals class for use program-wide
"""

from configparser import ConfigParser
from tto_debugger import TtoDebugger


class TtoGlobals:
    def __init__(self, config_file="tto.cfg"):
        self.debugger = TtoDebugger()
        self.debugger.message("INFO", "Started debugger")

        self.config = ConfigParser()
        self.config['DEFAULT'] = {'MidiOutEnabled': 'False'}
        self.config['tto'] = {}

        self.debugger.message("INFO", "Loading config file: {}".format(
            config_file))
        self.config.read(config_file)
        self.debugger.message("INFO", "Config Sections: {}".format(
            self.config.sections()))
        for key in self.config['tto']:
            self.debugger.message("INFO", "    Key: {}, Value: {}".format(
                key, self.config['tto'][key]))


tto_globals = TtoGlobals()  # Globally instanciate TtoGlobals
