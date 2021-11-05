"""
tto_globals - program globals for tto

This module handles program-wide globals, other variables, data, machine
states, etc for tto.


Requirements
------------
configparser : Basic configuration language parser.
tto_debugger : Error and info message handler for tto.

Classes
-------
tbd : tbd

Functions
---------
config_file_load : Accepts a (config_file) and attempts to load config options.

Variables
---------
debugger : Global instance of TtoDebugger class for logging.
config : Global instance of configparser containing program options.
midi: If MIDI enabled, global instance of TtoMidi for message handling.
"""

from configparser import ConfigParser
from tto_debugger import TtoDebugger


def config_file_load(config_file):
    global debugger
    global config
    debugger.message("INFO", "Loading config file: {}".format(
        config_file))
    config.read(config_file)
    debugger.message("INFO", "Config Sections: {}".format(
        config.sections()))
    for key in config['tto']:
        debugger.message("INFO", "    Key: {}, Value: {}".format(
            key, config['tto'][key]))


debugger = TtoDebugger()

config = ConfigParser()
config['DEFAULT'] = {'MidiOutEnabled': 'False'}
config['DEFAULT'] = {'MidiOutPort': 'wavestate 1 In'}
config['DEFAULT'] = {'MidiInEnabled': 'False'}
config['DEFAULT'] = {'MidiInPort': 'USB Midi '}
config['tto'] = {}

config_file_load("tto.cfg")

midi = None
