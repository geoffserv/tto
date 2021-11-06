"""
tto_midi - MIDI message handler for tto

This module handles midi messages received and produced during tto runtime.


Requirements
------------
tto_globals : Program-wide global variable module for tto.
tto_debugger : Error and info message handler for tto.
mido : A library for working with MIDI message and ports.
python-rtmidi : rtmidi backend for mido.
time : to calculate math around bpm

Classes
-------
TtoMidi : MIDI class for tto.
"""

import mido
import tto_globals
import time


class TtoMidi(object):
    def __init__(self):
        self.ports = {}

        self.channel_out = 0  # 0-15, but in the Real World it's 1-16
        self.channel_in = 0

        self.detect_midi_ports()

        self.ppb = 24  # 24 Pulses Per Beat through MIDI clock

        self.transport_playing = False

        # For
        self.downbeat_whole = False  # self.ppb mod self.ppb
        self.downbeat_half = False  # self.ppb mod (self.ppb / 2)
        self.downbeat_quarter = False  # self.ppb mod (self.ppb / 4)

        self.clock_pulses = 0
        self.clock_pulse_timestamp = time.time()
        self.clock_pulse_delta = 0

        self.bpm_detected = 0

        for midi_direction in ("In", "Out"):
            midi_port_config_attrib_enabled = "Midi{}Enabled".format(
                midi_direction)
            midi_port_config_attrib_name = "Midi{}Port".format(midi_direction)
            if tto_globals.config['tto'].getboolean(
                    midi_port_config_attrib_enabled):

                tto_globals.debugger.message("MIDI", "MIDI {} Enabled".format(
                    midi_direction))

                self.port_open(midi_port_config_attrib_name, midi_direction)

    def detect_midi_ports(self):
        if tto_globals.config['tto'].getboolean('MidiInEnabled'):
            tto_globals.debugger.message("MIDI", "Current MIDI Channel In: {}".
                                         format(self.channel_in + 1))
            tto_globals.debugger.message("MIDI", "MIDI In Ports Detected: {}".
                                         format(mido.get_input_names()))

        if tto_globals.config['tto'].getboolean('MidiOutEnabled'):
            tto_globals.debugger.message("MIDI",
                                         "Current MIDI Channel Out: {}".
                                         format(self.channel_out + 1))
            tto_globals.debugger.message("MIDI", "MIDI Out Ports Detected: {}".
                                         format(mido.get_output_names()))

    def port_open(self, midi_port_config_attrib_name, direction):
        midi_port_name = tto_globals.config['tto'][
            midi_port_config_attrib_name].strip('"')

        tto_globals.debugger.message("MIDI",
                                     "    Opening MIDI {}: '{}'".format(
                                         direction, midi_port_name))
        try:
            if direction == "In":
                self.ports[midi_port_config_attrib_name] = mido.open_input(
                    midi_port_name)
            if direction == "Out":
                self.ports[midi_port_config_attrib_name] = mido.open_output(
                    midi_port_name)

            tto_globals.debugger.message("MIDI",
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
                tto_globals.debugger.message("MIDI",
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
        if "MidiInPort" in self.ports:
            for midi_msg in self.ports["MidiInPort"].iter_pending():

                # Relay Midi IN to Midi OUT (passthrough to the synth)
                if "MidiOutPort" in self.ports:
                    self.ports["MidiOutPort"].send(midi_msg)

                # Handle clock-related stuff:
                if midi_msg.type in ("clock",
                                     "songpos",
                                     "start",
                                     "continue",
                                     "stop",
                                     "reset"):
                    self.handle_clock(midi_msg)

    def handle_clock(self, midi_msg):
        if midi_msg.type in ("start", "continue"):
            tto_globals.debugger.message("MIDI", "Playing message: {}".format(
                midi_msg))
            self.transport_playing = True

        if midi_msg.type in ("stop", "reset"):
            tto_globals.debugger.message("MIDI", "Stopped message: {}".format(
                midi_msg))
            self.transport_playing = False
            self.clock_pulses = 0

        if midi_msg.type == "clock":
            self.transport_playing = True  # If we got a clock, we're playing.

            # Turn off all downbeat booleans.
            self.downbeat_whole = False
            self.downbeat_half = False
            self.downbeat_quarter = False

            # If it's a downbeat frame it will now be switched True and
            # remain True
            # until execution passes this point again

            self.clock_pulses = (self.clock_pulses + 1) % self.ppb

            if (self.clock_pulses % self.ppb) == 1:
                self.downbeat_whole = True

                # Move the prior recorded timestamp to _delta,
                self.clock_pulse_delta = self.clock_pulse_timestamp
                # Then update the timestamp,
                self.clock_pulse_timestamp = time.time()

                # Then subtract the timestamp and delta and calculate bpm
                # Div by 60 cause 60 secs in a min
                self.bpm_detected = 60 / (self.clock_pulse_timestamp -
                                          self.clock_pulse_delta)

                tto_globals.debugger.message("MIDI",
                                             "Clock Downbeat: {} bpm detected".
                                             format(self.bpm_detected))

            if (self.clock_pulses % int(self.ppb / 2)) == 1:
                self.downbeat_half = True

            if (self.clock_pulses % int(self.ppb / 4)) == 1:
                self.downbeat_quarter = True
