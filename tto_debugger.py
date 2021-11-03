"""
tto_debugger - error and info message handler for tto

This module handles error and info messages produced during tto runtime.


Requirements
------------
time : needed to timestamp events and track execution times

Classes
-------
TtoDebugger : logging class for tto.
"""

import time


class TtoDebugger:
    def __init__(self):
        self.stats = {}
        self.messages = []
        self.printEnabled = True
        # https://docs.python.org/3/library/time.html#time.strftime
        self.time_format = "%Y-%m-%d %H:%M:%S"

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

    def message(self, severity, message):
        timestamp = time.time()
        self.messages.append({"severity": severity,
                              "message": message,
                              "timestamp": timestamp})
        if self.printEnabled:
            message_string = "{}- {}".format(severity, message)
            print(time.strftime(self.time_format, time.localtime(timestamp)),
                  message_string)

    def summary(self):
        for stat in self.stats:
            self.message("DEBUG SUMMARY",
                         "{}: {}".format(stat, self.stats[stat]))
        self.message("DEBUG SUMMARY",
                     "Runtime: {} seconds".format((
                             self.messages[-1]["timestamp"] -
                             self.messages[0]["timestamp"])))

    def progress(self, processed, total):
        if self.printEnabled:
            if (processed == 1) or (processed % 1000 == 0):
                percent_complete = int((processed / total) * 100)
                print("\r", end="")
                print("PROGRESS- Estimated build progress:",
                      percent_complete, "%", end="")
            if processed == total:
                print(" ... Done.")
