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
from tto_key import Key


debugger = TtoDebugger()  # Program-wide logger and debugger object

config = ConfigParser()  # Program-wide configuration object

key = Key()  # Program-wide music math object


def config_file_load(config_file):
    debugger.message("INFO", "Loading config file: {}".format(
        config_file))
    config.read(config_file)
    debugger.message("INFO", "Config Sections: {}".format(
        config.sections()))
    for cay in config['tto']:
        debugger.message("INFO", "    Key: {}, Value: {}".format(
            cay, config['tto'][cay]))


# These defaults apply unless overridden in the config file ['tto'] section:
config['DEFAULT'] = {'MidiOutEnabled': 'False'}
config['DEFAULT'] = {'MidiOutPort': 'wavestate 1 In'}
config['DEFAULT'] = {'MidiInEnabled': 'False'}
config['DEFAULT'] = {'MidiInPort': 'USB Midi '}
config['DEFAULT'] = {'FullScreen': 'True'}
config['DEFAULT'] = {'CanvasWidth': '1920'}
config['DEFAULT'] = {'CanvasHeight': '1080'}
config['DEFAULT'] = {'GraphicsEnabled': 'True'}
config['DEFAULT'] = {'Powermate': 'False'}
# Create a ['tto'] section containing the above defaults:
config['tto'] = {}

# Load the config file values overtop of the defaults above:
config_file_load("tto.cfg")

# Define some colors for convenience and readability
color_black = (0, 0, 0)
color_white = (64, 23, 4)
color_red = (255, 0, 0)
color_orange = (255, 94, 19)
color_orange_25 = (64, 23, 4)
color_orange_50 = (128, 47, 9)
color_orange_75 = (191, 69, 13)

# If I try to render things like text, corners of polygons, etc right up
# against the edge of a surface, then there is often clipping.  So, track
# a global canvas_margin to offset all coordinate systems and give some
# empty space around the edges of each surface.
# Define a default canvas_margin:
canvas_margin = 10

# tto program-wide events are added to the tto_globals.events dict,
# typically by the pygame module handle_input method.
# Most commonly, KEYDOWN / KEYUP.
# But, any module could add or view events if needed.
# At the end of each main loop run, this will be erased.  Each
# module in the main loop had a chance to inspect and action on any
# necessary events.
#
# The dict key is just an informative label and helps dedup events to prevent
# redundant entries.
# The dict is unordered but these events are also unordered- they're detected
# once per main loop execution, acted upon once per main loop execution, and
# cleared at the end.  In that sense, all we know is that they happened since
# the last main loop execution.
events = {}
# Big contributors to events: tto_pygame.TtoPygame.handle_input_key()
# Consumers: every GUISurface object's update_control()
# Known structures and values of events contents:
#    {'type': event_type,
#     'keycode': event.key,
#     'event': pygame.event}
# 'type' is one of:
#    'NA' = Unknown event type
#    'KU' = KeyUp with keycode in 'keycode'
#    'KD' = KeyDown with keycode in 'keycode'

running = False  # Main loop running boolean.  Set to false and program ends.

midi = None  # None until this is set-up by tto.py

pygame = None  # None until set-up by tto.py
