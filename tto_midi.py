"""
tto_midi - MIDI message handler for tto

This module handles midi messages received and produced during tto runtime.


Requirements
------------
tto_globals : Program-wide global variable module for tto.
tto_debugger : Error and info message handler for tto.
mido : A library for working with MIDI message and ports.
python-rtmidi : rtmidi backend for mido.

Classes
-------
TtoMidi : MIDI class for tto.
"""

import mido
import tto_globals


class TtoMidi(object):
    def __init__(self):
        port_out = None
        port_in = None

        if tto_globals.config['tto'].getboolean('MidiOutEnabled'):
            tto_globals.debugger.message("INFO", "MIDI OUT Enabled")
            tto_globals.debugger.message("INFO", "    OUT Ports: {}".format(
                mido.get_output_names()))
            tto_globals.debugger.message("INFO",
                                         "    Attempting to open: {}".format(
                                             tto_globals.config['tto']
                                             ['MidiOutPort']))
            try:
                self.port_out = mido.open_output(tto_globals.config['tto']
                                                 ['MidiOutPort'].strip('"'))
                tto_globals.debugger.message("INFO",
                                             "    Successfully opened OUT")
            except Exception as e:
                tto_globals.debugger.message("EXCEPTION",
                                             "Opening MIDI OUT: {}".format(e))
                tto_globals.debugger.exit(
                    "MIDI OUT enabled but could not open port.")

        if tto_globals.config['tto'].getboolean('MidiInEnabled'):
            tto_globals.debugger.message("INFO", "MIDI IN Enabled")
            tto_globals.debugger.message("INFO", "    IN Ports: {}".format(
                mido.get_input_names()))
            tto_globals.debugger.message("INFO",
                                         "    Attempting to open: {}".format(
                                             tto_globals.config['tto']
                                             ['MidiInPort']))
            try:
                self.port_out = mido.open_input(tto_globals.config['tto']
                                                 ['MidiInPort'].strip('"'))
                tto_globals.debugger.message("INFO",
                                             "    Successfully opened IN")
            except Exception as e:
                tto_globals.debugger.message("EXCEPTION",
                                             "Opening MIDI IN: {}".format(e))
                tto_globals.debugger.exit(
                    "MIDI IN enabled but could not open port.")

