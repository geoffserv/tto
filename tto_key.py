"""
tto_key - key, scale, and chord data class for tto

This class handles music math for tto.  It's instanciated in tto_globals and
available program-wide.


Requirements
------------
tto_globals : Program-wide global variable module for tto.

Classes
-------
Key : key, scale, and chord data class

Functions
---------
none : none

Variables
---------
none : none
"""

import tto_globals


class Key(object):
    def __init__(self):
        # current_key is 0-11
        self.current_key = 0

        # current_scale_degree is 0-6
        self.current_scale_degree = 0

        self.notes_on = {}  # dict containing key.notes indices currently
        # playing 0-11

        self.keyboard_keys_down = {}  # dict containing event keycodes which
        # previously triggered a keydown.  So they're presumably still down.
        # Later when a key is lifted, check the keycode against this to
        # figure out the key & scale degree back when it was triggered,
        # so it's possible to know which thing to now turn off.
        # [keycode] = target_note

        # 12 tones arranged by fifths and their piano keyboard key kbNum 0-11
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

        # Diatonic fifths, their associated triad chords and scale degree modes
        self.fifths = {11: {"step": 4,
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

        # Around the circle of fifths, diatonic tones are position 0-5, 11
        self.diatonic = [0, 1, 2, 3, 4, 5, 11]

        self.chord_scale = [0, 1, 2, 3, 4, 5, 11]
        self.key_scale_ordered = [0, 2, 4, 11, 1, 3, 5]

    def set_key(self, new_key):
        tto_globals.debugger.message(
            "KEY_",
            "Set Scale Degree to {}".format(new_key)
        )
        self.current_key = new_key

    def set_scale_degree(self, scale_degree):
        tto_globals.debugger.message(
            "KEY_",
            "Set Scale Degree to {}".format(scale_degree)
        )
        self.current_scale_degree = scale_degree

    def trigger(self, note_index, keycode, mode="play"):

        # The keyboard will be sending an index of note from the key binding
        # Need to add the scale degree and wrap at 7 because the scale will be
        # 0-6 (7 tones)
        target_note = ((note_index +
                        self.current_scale_degree)
                       % 7)
        # If it's 6, it's 11.  We skip the non-diatonics 6,7,8,9,10
        if target_note == 6:
            target_note = 11

        # now offset by the key and wrap at 12.  all chromatic tones are 0-11
        target_note = (target_note + self.current_key) % 12

        tto_globals.debugger.message(
            "KEY_",
            "Mode {}, k_code {}, index {}, s_degree {}, key {} = t_note {}".
            format(mode,
                   keycode,
                   note_index,
                   self.current_scale_degree,
                   self.current_key,
                   target_note)
        )

        if mode == "play":
            if target_note not in self.notes_on:
                self.notes_on[target_note] = True
                self.keyboard_keys_down[keycode] = target_note

        if mode == "stop":
            #if target_note in self.notes_on:
            #    del self.notes_on[target_note]
            if keycode in self.keyboard_keys_down:
                del self.notes_on[self.keyboard_keys_down[keycode]]
                del self.keyboard_keys_down[keycode]