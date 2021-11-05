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
        self.ports = {}

        self.channel_out = 0  # 0-15, but in the Real World it's 1-16
        self.channel_in = 0

        self.detect_midi_ports()

        for midi_direction in ("In", "Out"):
            midi_port_config_attrib_enabled = "Midi{}Enabled".format(
                midi_direction)
            midi_port_config_attrib_name = "Midi{}Port".format(midi_direction)
            if tto_globals.config['tto'].getboolean(
                    midi_port_config_attrib_enabled):

                tto_globals.debugger.message("INFO", "MIDI {} Enabled".format(
                    midi_direction))

                self.port_open(midi_port_config_attrib_name, midi_direction)

    def detect_midi_ports(self):
        if tto_globals.config['tto'].getboolean('MidiInEnabled'):
            tto_globals.debugger.message("INFO", "Current MIDI Channel In: {}".
                                         format(self.channel_in + 1))
            tto_globals.debugger.message("INFO", "MIDI In Ports Detected: {}".
                                         format(mido.get_input_names()))

        if tto_globals.config['tto'].getboolean('MidiOutEnabled'):
            tto_globals.debugger.message("INFO",
                                         "Current MIDI Channel Out: {}".
                                         format(self.channel_out + 1))
            tto_globals.debugger.message("INFO", "MIDI Out Ports Detected: {}".
                                         format(mido.get_output_names()))

    def port_open(self, midi_port_config_attrib_name, direction):
        midi_port_name = tto_globals.config['tto'][
            midi_port_config_attrib_name].strip('"')

        tto_globals.debugger.message("INFO",
                                     "    Opening MIDI {}: '{}'".format(
                                         direction, midi_port_name))
        try:
            if direction == "In":
                self.ports[midi_port_config_attrib_name] = mido.open_input(
                    midi_port_name)
            if direction == "Out":
                self.ports[midi_port_config_attrib_name] = mido.open_output(
                    midi_port_name)

            tto_globals.debugger.message("INFO",
                                         "    Successfully opened: '{}'".
                                         format(midi_port_name))
        except Exception as e:
            tto_globals.debugger.message("EXCEPTION",
                                         "Opening '{}': {}".format(
                                             midi_port_name, e))
            tto_globals.debugger.exit(
                "'{}' specified in .cfg file, but could not open port.".format(
                    midi_port_name))

    def ports_close(self):
        for port in self.ports:
            try:
                tto_globals.debugger.message("INFO",
                                             "Closing MIDI port {}".format(
                                                 port))
                self.ports[port].close()
            except Exception as e:
                tto_globals.debugger.message("EXCEPTION",
                                             "Error closing MIDI port {}: {}".
                                             format(port, e))

    def handle_messages(self):
        # Non-blocking method run once per main-loop execution cycle
        # Handle everything needed for MIDI during the course of normal runtime

        # Process incoming MIDI
        if self.ports and "MidiInPort" in self.ports:
            for midi_msg in self.ports["MidiInPort"].iter_pending():

                # Handle clock-related stuff:
                if midi_msg.type == "clock" or \
                                    "songpos" or \
                                    "start" or \
                                    "continue" or \
                                    "stop" or \
                                    "reset":
                    self.handle_clock(midi_msg)

    def handle_clock(self, midi_msg):
        # MIDI generally will send 24 PPQ (pulses per quarter)
        tto_globals.debugger.log_stat("MidiInMsgsTypeClockTotal", 1)

