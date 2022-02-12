"""tto_midi - MIDI message handler for tto

This module handles midi messages received and produced during tto runtime.


Requirements
------------
tto_globals : Program-wide global variable module for tto.
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

        self.channel_out = 0  # 0-15, but in the Real World it's 1-16. So add 1
        self.channel_in = 0

        # Show MIDI port names in the console logs
        self.detect_midi_ports()

        # 24 Pulses Per Beat (ppb) through MIDI clock is the default.
        # I've read that DAWs can be reconfigurable even up to e.g. 192 ppb
        self.ppb = 24

        # If transport_playing, my best guess from the MIDI I'm seeing is that
        # the upstream DAW connected to my MIDI-in is in 'playing' state
        self.transport_playing = False

        # A bit to track whether a new transport MIDI message has been seen.
        # For ex, set to False, then check if it's True.  if so,
        # a message has been seen by the midi module in the meantime.
        self.transport_new_messages = False

        # The heart of the clock is clock_pulses.
        # Each time we receive a MIDI clock message, this increments
        # When this is equal to the ppb, one beat has elapsed
        self.clock_pulses = 0

        # Three bits will allow me to track at a resolution of 1/16-notes.
        self.downbeat_whole = False  # clock_pulses mod self.ppb == 1
        self.downbeat_half = False  # clock_pulses mod (self.ppb / 2) == 1
        self.downbeat_quarter = False  # clock_pulses mod (self.ppb / 4) == 1

        # Attributes used for MIDI clock bpm math
        self.clock_pulse_timestamp = time.time()
        self.clock_pulse_delta = time.time()
        self.bpm_detected = 0

        # Check the program config options and attempt to open MIDI ports if
        # they are enabled.  We need an In for receiving upstream MIDI, and
        # an Out to relaying that MIDI downstream + our own inserted messages:

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
        """Informational method to log MIDI port names detected on the system.

        On some systems, the port name will change depending on the order
        in which MIDI devices are attached.  So, I'm frequently needing to
        update the cfg file with the days' relevant MIDI port name.  This
        method just helps keep me updated on status during program startup.
        """

        try:
            if tto_globals.config['tto'].getboolean('MidiInEnabled'):
                tto_globals.debugger.message("MIDI",
                                             "Current MIDI Channel In: {}".
                                             format(self.channel_in + 1))
                tto_globals.debugger.message("MIDI",
                                             "MIDI In Ports Detected: {}".
                                             format(mido.get_input_names()))

            if tto_globals.config['tto'].getboolean('MidiOutEnabled'):
                tto_globals.debugger.message("MIDI",
                                             "Current MIDI Channel Out: {}".
                                             format(self.channel_out + 1))
                tto_globals.debugger.message("MIDI",
                                             "MIDI Out Ports Detected: {}".
                                             format(mido.get_output_names()))
        except Exception as e:
            tto_globals.debugger.message("EXCEPTION",
                                         "Error detecting MIDI port names: {}".
                                         format(e))

    def port_open(self, midi_port_config_attrib_name, direction):
        try:
            midi_port_name = tto_globals.config['tto'][
                midi_port_config_attrib_name].strip('"')

            tto_globals.debugger.message("MIDI",
                                         "    Opening MIDI {}: '{}'".format(
                                             direction, midi_port_name))
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

    def port_out_panic(self):
        if "MidiOutPort" in self.ports:
            try:
                tto_globals.debugger.message("MIDI",
                                             "Sending panic() to MIDI Out")
                self.ports["MidiOutPort"].panic()
            except Exception as e:
                tto_globals.debugger.message("EXCEPTION",
                                             "Error sending panic(): {}".
                                             format(e))

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

        # Process incoming MIDI In, handle clock, and relay to MIDI Out ASAP
        try:
            if "MidiInPort" in self.ports:
                for midi_msg in self.ports["MidiInPort"].iter_pending():

                    # Relay MIDI In to MIDI Out
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
        except Exception as e:
            tto_globals.debugger.message("EXCEPTION",
                                         "Error processing MIDI: {}".
                                         format(e))

    def transport_play(self, midi_msg=None):
        tto_globals.debugger.message("MIDI",
                                     "transport_playing TRUE: {}".format(
                                         midi_msg))
        self.transport_playing = True
        self.transport_new_messages = True

    def transport_stop(self, midi_msg=None):
        tto_globals.debugger.message("MIDI",
                                     "transport_playing FALSE: {}".format(
                                         midi_msg))
        self.transport_playing = False
        self.transport_new_messages = True
        self.clock_pulses = 0

    def send(self, note, mode="stop"):
        mido_message = "note_off"
        velocity = 0
        if mode == "play":
            mido_message = "note_on"
            velocity = 100

        tto_globals.debugger.message("MIDI",
                                     "send: {}, vel: {}, mido_msg: {}".format(
                                         note, velocity, mido_message))

        midi_msg = mido.Message(mido_message,
                                channel=self.channel_out,
                                note=note,
                                velocity=velocity)

        try:
            if "MidiOutPort" in self.ports:
                self.ports["MidiOutPort"].send(midi_msg)

        except Exception as e:
            tto_globals.debugger.message("EXCEPTION",
                                         "Error processing MIDI: {}".
                                         format(e))

    def handle_clock(self, midi_msg):
        if midi_msg.type in ("start", "continue"):
            self.transport_play(midi_msg)

        if midi_msg.type in ("stop", "reset"):
            self.transport_stop(midi_msg)

        if midi_msg.type == "clock":
            if not self.transport_playing:
                # If we got a clock, we're playing.  If we don't think we're
                # playing yet, then lets start thinking that we're playing:
                self.transport_play(midi_msg)

            # Turn off all downbeat booleans.
            self.downbeat_whole = False
            self.downbeat_half = False
            self.downbeat_quarter = False

            # If it's a downbeat frame it will now be switched True and
            # remain True
            # until execution passes this point again, e.g. for one entire
            # MIDI clock pulse duration, e.g. for one 'frame' of midi clock
            # resolution.

            self.clock_pulses = (self.clock_pulses + 1) % self.ppb

            if (self.clock_pulses % self.ppb) == 1:
                self.downbeat_whole = True

                # Move the prior recorded timestamp to _delta,
                self.clock_pulse_delta = self.clock_pulse_timestamp
                # Then update the timestamp,
                self.clock_pulse_timestamp = time.time()

                # Then subtract the timestamp and delta and calculate bpm
                # Div 60, because 60 secs in a min
                self.bpm_detected = 60 / (self.clock_pulse_timestamp -
                                          self.clock_pulse_delta)

                tto_globals.debugger.message("MIDI",
                                             "Clock Downbeat: {} bpm detected".
                                             format(self.bpm_detected))

            if (self.clock_pulses % int(self.ppb / 2)) == 1:
                self.downbeat_half = True

            if (self.clock_pulses % int(self.ppb / 4)) == 1:
                self.downbeat_quarter = True
                self.transport_new_messages = True
