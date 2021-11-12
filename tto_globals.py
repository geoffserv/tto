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


debugger = TtoDebugger()  # Program-wide logger and debugger

config = ConfigParser()  # Program-wide configuration
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

keyboard_cols = 12
keyboard_rows = 4

# keyboard_layout is a list of lists,
# keyboard_layout[] represents each row
# keyboard_layout[][] is the cols
# within which is a dict representing the key, labels, actions, etc
# Initialize a default layout
keyboard_layout = []
for row in range(keyboard_rows):
    keyboard_layout.append([])
    for col in range(keyboard_cols):
        keyboard_layout[row].append(
            {
                'keyboard_code': 0,
                'button_label_default': "",
                'button_label_1': "",
                'button_label_2': "",
                'button_label_3': "",
                'button_color_bg': color_black,
                'button_color_bg_default': color_black,
                'button_color_bg_on': color_orange_50,
                'button_color_fg': color_orange_50,
                'button_color_fg_default': color_orange_50
             }
        )

# Set-up row 1
# Key signature / Tone class / Tonal root
i = 0
for button_default_label in ('C', 'G', 'D', 'A', 'E', 'B',
                             'Gb', 'Db', 'Ab', 'Eb', 'Bb',
                             'F'):
    keyboard_layout[0][i]['button_label_default'] = button_default_label
    keyboard_layout[0][i]['button_label_1'] = button_default_label
    i += 1
i = 0
#                              bg_color   , fg_color
for button_default_colors in ((color_white, color_black),  # C
                              (color_white, color_black),  # G
                              (color_white, color_black),  # D
                              (color_white, color_black),  # A
                              (color_white, color_black),  # E
                              (color_white, color_black),  # B
                              (color_black, color_orange_50),  # Gb
                              (color_black, color_orange_50),  # Db
                              (color_black, color_orange_50),  # Ab
                              (color_black, color_orange_50),  # Eb
                              (color_black, color_orange_50),  # Bb
                              (color_white, color_black)):  # F
    keyboard_layout[0][i]['button_color_bg'] = button_default_colors[0]
    keyboard_layout[0][i]['button_color_bg_default'] = \
        button_default_colors[0]
    keyboard_layout[0][i]['button_color_fg'] = button_default_colors[1]
    keyboard_layout[0][i]['button_color_fg_default'] = \
        button_default_colors[1]
    i += 1

# Set-up row 2
i = 0
for button_default_label in (1, 5, 2, 6, 3, 7, 4, 1, 5, 2, 6, 3):
    keyboard_layout[1][i]['button_label_default'] = button_default_label
    keyboard_layout[1][i]['button_label_1'] = button_default_label
    i += 1
i = 0
#                              bg_color   , fg_color
for button_default_colors in ((color_white, color_black),  # 1
                              (color_white, color_black),  # 5
                              (color_black, color_orange_50),  # 2
                              (color_black, color_orange_50),  # 6
                              (color_black, color_orange_50),  # 3
                              (color_black, color_orange_50),  # 7
                              (color_white, color_black),  # 4
                              (color_white, color_black),  # 1
                              (color_white, color_black),  # 5
                              (color_black, color_orange_50),  # 2
                              (color_black, color_orange_50),  # 6
                              (color_black, color_orange_50)):  # 3
    keyboard_layout[1][i]['button_color_bg'] = button_default_colors[0]
    keyboard_layout[1][i]['button_color_bg_default'] = \
        button_default_colors[0]
    keyboard_layout[1][i]['button_color_fg'] = button_default_colors[1]
    keyboard_layout[1][i]['button_color_fg_default'] = \
        button_default_colors[1]
    i += 1

# Set-up row 3
i = 0
for button_default_label in (1, 5, 2, 6, 3, 7, 4, 1, 5, 2, 6, 3):
    keyboard_layout[2][i]['button_label_default'] = button_default_label
    keyboard_layout[2][i]['button_label_1'] = button_default_label
    i += 1
i = 0
#                              bg_color   , fg_color
for button_default_colors in ((color_white, color_black),  # 1
                              (color_white, color_black),  # 5
                              (color_black, color_orange_50),  # 2
                              (color_black, color_orange_50),  # 6
                              (color_white, color_black),  # 3
                              (color_black, color_orange_50),  # 7
                              (color_black, color_orange_50),  # 4
                              (color_white, color_black),  # 1
                              (color_white, color_black),  # 5
                              (color_black, color_orange_50),  # 2
                              (color_black, color_orange_50),  # 6
                              (color_white, color_black)):  # 3
    keyboard_layout[2][i]['button_color_bg'] = button_default_colors[0]
    keyboard_layout[2][i]['button_color_bg_default'] = \
        button_default_colors[0]
    keyboard_layout[2][i]['button_color_fg'] = button_default_colors[1]
    keyboard_layout[2][i]['button_color_fg_default'] = \
        button_default_colors[1]
    i += 1

# Set-up row 4
i = 0
for button_default_label in range(12):
    keyboard_layout[3][i]['button_label_default'] = 'fn'
    keyboard_layout[3][i]['button_label_1'] = 'fn'
    keyboard_layout[3][i]['button_color_bg'] = color_white
    keyboard_layout[3][i]['button_color_bg_default'] = color_white
    keyboard_layout[3][i]['button_color_fg'] = color_black
    keyboard_layout[3][i]['button_color_fg_default'] = color_black
    i += 1

button_keyboard_codelist = \
    (96,  49,  50,  51,  52,  53,  54,  55,  56,  57,  48, 45,
     113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93,
     97,  115, 100, 102, 103, 104, 106, 107, 108, 59,  39, 13,
     1073742049,  # left shift key code
          122, 120, 99,  118, 98,  110, 109, 44,  46,  47, 1073742053  # r shft
     )

# button_keyboard_codes is indexed against the keyboard code and contains
# a tuple of where within keyboard_layout that button's attributes are found.
# Useful for associating a keyboard event with the keyboard_layout options
# related to that button in a GUISurface update_control() etc
button_keyboard_codes = {}
i = 0
for row in range(keyboard_rows):
    for col in range(keyboard_cols):
        button_keyboard_codes[button_keyboard_codelist[i]] = (row, col)
        i += 1

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

# Labels used around the circle
note_wheel_labels = {11: {"step": 4,
                          "triad": "MAJ",
                          "mode": "Lydian"},
                     0: {"step": 1,
                         "triad": "MAJ",
                         "mode": "Ionian"},
                     1: {"step": 5,
                         "triad": "MAJ",
                         "mode": "Mixolydian"},
                     2: {"step": 2,
                         "triad": "min",
                         "mode": "Dorian"},
                     3: {"step": 6,
                         "triad": "min",
                         "mode": "Aeolian"},
                     4: {"step": 3,
                         "triad": "min",
                         "mode": "Phrygian"},
                     5: {"step": 7,
                         "triad": "dim",
                         "mode": "Locrian"},
                     }


class Key(object):
    def __init__(self):
        self.current_key = 0
        self.current_chord_root = 0
        self.current_key_mode = 0
        self.notes_on = []  # List containing key.notes indices currently
        # playing 0-11

        self.notes = [
            {'noteName': 'C', 'sharpName': 'C', 'kbNum': 0},
            {'noteName': 'G', 'sharpName': 'G', 'kbNum': 7},
            {'noteName': 'D', 'sharpName': 'D', 'kbNum': 2},
            {'noteName': 'A', 'sharpName': 'A', 'kbNum': 9},
            {'noteName': 'E', 'sharpName': 'E', 'kbNum': 4},
            {'noteName': 'B', 'sharpName': 'B', 'kbNum': 11},
            {'noteName': 'Gb', 'sharpName': 'F#', 'kbNum': 6},
            {'noteName': 'Db', 'sharpName': 'C#', 'kbNum': 1},
            {'noteName': 'Ab', 'sharpName': 'G#', 'kbNum': 8},
            {'noteName': 'Eb', 'sharpName': 'D#', 'kbNum': 3},
            {'noteName': 'Bb', 'sharpName': 'A#', 'kbNum': 10},
            {'noteName': 'F', 'sharpName': 'E#', 'kbNum': 5}
                    ]

        self.diatonic = [0, 1, 2, 3, 4, 5, 11]
        self.chord_scale = [0, 1, 2, 3, 4, 5, 11]
        self.key_scale_ordered = [0, 2, 4, 11, 1, 3, 5]

    def update_diatonic(self):
        self.diatonic = []
        for i in [0, 1, 2, 3, 4, 5, 11]:
            self.diatonic.append(
                (self.current_key + i) % 12
            )

    def update_chord_scale(self):
        self.chord_scale = []
        for i in range(self.current_key_mode, self.current_key_mode + 7):
            self.chord_scale.append(self.diatonic[i % 7])

    def rotate_key(self, add_by=0):
        self.current_key += add_by
        self.current_key = self.current_key % 12  # Rollover range 0-11
        self.update_diatonic()

    def rotate_key_mode(self, add_by=0):
        self.current_key_mode += add_by
        self.current_key_mode = self.current_key_mode % 7

    def rotate_chord(self, add_by=0, set_to=None):
        self.current_chord_root += add_by

        if set_to is not None:
            self.current_chord_root = set_to

        self.current_chord_root = self.current_chord_root % 12  # Rollover ...

        self.update_chord_scale()

    def calculate_chord(self, chord_def):
        chord = []
        for note in chord_def:
            chord.append(self.chord_scale[chord_slices_dict[note]])
        return chord


# For now, how intervals are defined:
# The 'slice number' around the circle of fifths
# 0 = Root
# 1 = Fifth
# 2 = Second
# 3 = Sixth
# 4 = Third
# 5 = Seventh
# 6 = Fourth
chord_slices_dict = {1: 0,
                     2: 2,
                     3: 4,
                     4: 6,
                     5: 1,
                     6: 3,
                     7: 5}


key = Key()

running = False  # Main loop running boolean.  Set to false and program ends.

midi = None  # None until this is set-up by tto.py

pygame = None  # None until set-up by tto.py
