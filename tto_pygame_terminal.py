from tto_pygame_guisurface import GUISurface
from tto_shapes import *
import time


class GUISurfaceTerminal(GUISurface):
    def __init__(self, canvas_width, canvas_height, blit_x, blit_y, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(canvas_width, canvas_height,
                                             blit_x, blit_y, **kwargs)

        # 10 lines of logging shown by default
        self.log_lines = kwargs.get('log_lines', 10)

        # self.time_format for how to display timestamps on-screen
        # https://docs.python.org/3/library/time.html#time.strftime
        self.time_format = "%Y-%m-%d %H:%M:%S %z"

        # To prevent text screen runoff:
        self.log_lines_max_len = 94  # Truncate messages longer than this

    def draw_control(self):
        """ Overriding GUISurface.draw_control()
        """
        self.surface.fill(self.color_bg)
        self.draw_control_border()

        log_lines = tto_globals.debugger.messages[-self.log_lines:]

        line_spacing = int(self.canvas_height / self.log_lines)
        for i in range(self.log_lines):

            message_string = "{} {}- {}".\
                format(time.strftime(self.time_format,
                                     time.localtime(log_lines[i]
                                                    ['timestamp'])),
                       log_lines[i]['severity'],
                       log_lines[i]['message'])

            if len(message_string) > self.log_lines_max_len:
                message_string = "{} ...".format(
                    message_string[:(self.log_lines_max_len - 4)])

            self.draw_label(coordinates=(7, (i * line_spacing) + 5),
                            degrees=0,
                            text_label=message_string,
                            font=self.font,
                            color=tto_globals.color_orange,
                            align="left")

    def update_control(self):
        """ Overriding GUISurface.update_control()
        """
        self.needs_rendering = False
        if tto_globals.debugger.new_messages:
            self.needs_rendering = True
            tto_globals.debugger.new_messages = False
