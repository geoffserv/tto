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

Classes
-------
Tto : Main class for config, all gfx/midi/io, runtime, and shutdown of tto.
"""

from tto_globals import TtoGlobals


class Tto:
    def __init__(self):
        pass
