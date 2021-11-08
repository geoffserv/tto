"""tto - tonal organ

Interactive MIDI instrument organized around tone class and scale degree.

This project is an attempt to refactor the helm project from
<https://github.com/geoffserv/helm>.

Requirements
------------
tto_globals : Program-wide global variable module for tto
tto_midi : MIDI message handler for tto.
atexit : Trap exit conditions to handle program termination gracefully.

Functions
---------
tto_init() : Initialize environment for tto.
tto_run() : Run tto main loop
tto_terminate() : Gracefully terminate the program.
"""

import tto_globals
from tto_midi import TtoMidi
from tto_pygame import TtoPygame, pygame_terminate
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

    if tto_globals.pygame:
        pygame_terminate()

    # Show a debugger summary
    tto_globals.debugger.summary()

    tto_globals.debugger.exit("Completed program termination")


def tto_init():
    # Register the tto_terminate() function to run any time the program
    # terminates for any reason, using the atexit library.
    atexit.register(tto_terminate)

    # Instanciate a mido object and init MIDI
    tto_globals.midi = TtoMidi()

    # Instanciate a pygame object and init graphics
    tto_globals.pygame = TtoPygame()

    tto_globals.running = False  # Will be True once self.run() is called


def tto_run():
    tto_globals.debugger.message("INFO", "Entering run state")
    tto_globals.running = True

    while tto_globals.running:

        #################
        # Main run Loop #
        #################

        # Main run loop performance monitoring
        tto_globals.debugger.perf_monitor()

        # Poll user input, update pygame, and populate tto_globals.events
        tto_globals.pygame.handle_pygame()

        # Receive and send MIDI
        tto_globals.midi.handle_messages()

        # Clear the events dict.  All events should have been handled.
        tto_globals.events = {}

        #####################
        # End Main run Loop #
        #####################


if __name__ == "__main__":
    tto_init()
    tto_run()
