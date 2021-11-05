"""
tto - traugott tonal organ

Interactive MIDI instrument organized around tone class and scale degree.

This project is an attempt to refactor the helm project from
<https://github.com/geoffserv/helm>.  Helm proved to be interesting and
playable, but needs several fundamental interface changes to be easier
to use in a live musical environment, as well as many fundamental code
and structure improvements.

Requirements
------------
tto_globals : Program-wide global variable module for tto
tto_midi : MIDI message handler for tto.

Classes
-------
Tto : Main class for config, all gfx/midi/io, runtime, and shutdown of tto.
"""

import tto_globals
from tto_midi import TtoMidi


class Tto(object):
    def __init__(self):
        tto_globals.midi = TtoMidi()

        self.running = False  # Will be True once self.run() is called

    def run(self):
        tto_globals.debugger.message("INFO", "Entering run state")
        self.running = True

        while self.running:
            tto_globals.midi.forward_messages()


if __name__ == "__main__":
    tto = Tto()
    tto.run()