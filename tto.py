"""tto - tonal organ

Interactive MIDI instrument organized around tone class and scale degree.

This project is an attempt to refactor the helm project from
<https://github.com/geoffserv/helm>.

Requirements
------------
tto_globals : Program-wide global variable module for tto
tto_midi : MIDI message handler for tto.
atexit : Trap exit conditions to handle program termination gracefully.

Classes
-------
Tto : Main class for config, all gfx/midi/io, runtime, and shutdown of tto.
"""

import tto_globals
from tto_midi import TtoMidi
import atexit


def tto_terminate():
    """Gracefully terminate the program.

    This should try to handle any final cleanup and close any open resources
    before exiting the program entirely
    """

    tto_globals.debugger.message("INFO", "Beginning program termination")

    if tto_globals.midi:
        # panic() the MIDI out port to abruptly stop all sounding notes
        tto_globals.midi.port_out_panic()
        # Try to close all open MIDI ports
        tto_globals.midi.ports_close()

    # Show a debugger summary
    tto_globals.debugger.summary()

    tto_globals.debugger.exit("Completed program termination")


class Tto(object):
    def __init__(self):

        # Register the tto_terminate() function to run any time the program
        # terminates for any reason, using the atexit library.
        atexit.register(tto_terminate)

        # Instanciate a midi object and attach to tto_globals
        tto_globals.midi = TtoMidi()

        self.running = False  # Will be True once self.run() is called

    def run(self):
        tto_globals.debugger.message("INFO", "Entering run state")
        self.running = True

        while self.running:

            #################
            # Main run Loop #
            #################

            tto_globals.debugger.perf_monitor()  # Run loop perf monitoring

            tto_globals.midi.handle_messages()


if __name__ == "__main__":
    tto = Tto()
    tto.run()
