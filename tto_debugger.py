"""
tto_debugger - error and info message handler for tto

This module handles error and info messages produced during tto runtime.


Requirements
------------
time : Needed to timestamp events and track execution times.
sys : Allow the debugger to access exit() and others

Classes
-------
TtoDebugger : Logging class for tto.
"""

import time
import sys


class TtoDebugger(object):
    def __init__(self):
        self.stats = {}
        self.messages = []
        self.printEnabled = True

        # self.time_format for how to display timestamps on-screen
        # https://docs.python.org/3/library/time.html#time.strftime
        self.time_format = "%Y-%m-%d %H:%M:%S %z"

        self.message("INFO", "Started debugger")

        self.runtime_ticks = 0
        self.runtime_tick_time = time.time()
        self.runtime_mhz = 0

    def perf_monitor(self):
        # Non-blocking method run once per main-loop execution cycle
        # Tracks and reports loop execution speed
        sample_size = 1000000
        self.runtime_ticks += 1
        if self.runtime_ticks > sample_size:
            self.runtime_mhz = ((sample_size / (time.time() -
                                                self.runtime_tick_time)) /
                                1000000)
            self.message("CNTR", "(Counter) Main loop execution MHz: {}".
                         format(self.runtime_mhz))
            self.runtime_ticks = 0
            self.runtime_tick_time = time.time()

    def log_stat(self, statistic, increment: int, value=0):
        if statistic not in self.stats:
            self.stats[statistic] = int(increment) or int(value)
        else:
            self.stats[statistic] += int(increment)

    def get_stat(self, statistic):
        if statistic not in self.stats:
            return 0
        else:
            return int(self.stats[statistic])

    def report_stat(self, statistic, mod=100):
        if self.printEnabled and statistic in self.stats:
            if (self.stats[statistic] == 1) or \
                    (self.stats[statistic] % mod == 0):
                self.message("CNTR", "(Counter) {}: {}".format(
                    statistic, self.stats[statistic]))

    def message(self, severity, message):
        timestamp = time.time()
        self.messages.append({"severity": severity,
                              "message": message,
                              "timestamp": timestamp})
        if self.printEnabled:
            message_string = "{}- {}".format(severity, message)
            print(time.strftime(self.time_format, time.localtime(timestamp)),
                  message_string)

    def exit(self, message):
        self.message("EXIT", message)
        sys.exit(message)

    def summary(self):
        for stat in self.stats:
            self.message("DEBUG",
                         "{}: {}".format(stat, self.stats[stat]))
        self.message("DEBUG",
                     "Runtime: {} seconds".format((
                             self.messages[-1]["timestamp"] -
                             self.messages[0]["timestamp"])))

