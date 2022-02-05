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
        # self.notes_on[key_index] = (key, note, octave)
        #   key_index = index sent from tto_pygame_keyboardmap
        #   key = self.current_key at the time of triggering the note
        #   note = self.notes index at the time of triggering the note

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

    def trigger(self, note_index, mode="play"):

        # The keyboard will be sending an index of note from the key binding
        # Need to add the scale degree and wrap at 12 to play the chord
        #   notes according to the scale degree
        target_note = (note_index + self.current_scale_degree % 12)

        tto_globals.debugger.message(
            "KEY_",
            "target_note, Mode {}, value {}".format(mode, target_note)
        )

        if mode == "play":
            if target_note not in self.notes_on:
                pass
                # self.notes_on.append(target_note)

        if mode == "stop":
            if target_note in self.notes_on:
                pass
                # self.notes_on.remove(target_note)
