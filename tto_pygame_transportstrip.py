from tto_pygame_guisurface import GUISurface
from tto_shapes import *
import pygame


class GUISurfaceTransportStrip(GUISurface):
    def __init__(self, canvas_width, canvas_height, blit_x, blit_y, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(canvas_width, canvas_height,
                                             blit_x, blit_y, **kwargs)

        self.downbeat_whole_indicator = False
        self.downbeat_half_indicator = False
        self.downbeat_quarter_indicator = False

    def draw_control(self):
        """ Overriding GUISurface.draw_control()
        """
        self.surface.fill(self.color_bg)
        self.draw_control_border()

        # Clock Playing Box #
        play_message_string = "clock stopped"
        bpm = 0
        color = tto_globals.color_orange_50
        border = 1

        if tto_globals.midi and tto_globals.midi.transport_playing:
            play_message_string = "clock playing"
            bpm = round(tto_globals.midi.bpm_detected)
            color = tto_globals.color_orange
            border = 2
        rect_border = pygame.Rect(10, 10, 154, 30)
        pygame.draw.rect(self.surface, color,
                         rect_border, border)
        self.draw_label(coordinates=(87, 23),
                        degrees=0,
                        text_label=play_message_string,
                        font=self.font,
                        color=color,
                        align="center")

        # BPM Box #
        bpm_message_string = "{} BPM".format(bpm)
        rect_border = pygame.Rect(174, 10, 110, 30)
        pygame.draw.rect(self.surface, color,
                         rect_border, border)
        self.draw_label(coordinates=(227, 24),
                        degrees=0,
                        text_label=bpm_message_string,
                        font=self.font,
                        color=color,
                        align="center")

        # Beat Monitor #
        beatmon_message_string = "MIDI Clock"
        rect_border = pygame.Rect(294, 10, 214, 30)
        pygame.draw.rect(self.surface, color,
                         rect_border, border)
        self.draw_label(coordinates=(307, 15),
                        degrees=0,
                        text_label=beatmon_message_string,
                        font=self.font,
                        color=color,
                        align="left")

        # Beat Monitor "LED" squares that blink #
        # if self.downbeat_whole_indicator is False, border will be int 1
        #    otherwise border will be int 0.
        #    This way, if the indicator is true, border is 0 and the box
        #    is filled in.  Otherwise border is 1 and the box is outlined.
        border = (not self.downbeat_whole_indicator) * 1

        rect_border = pygame.Rect(420, 10, 30, 30)
        pygame.draw.rect(self.surface, color,
                         rect_border, border)

        border = (not self.downbeat_half_indicator) * 1

        rect_border = pygame.Rect(449, 10, 30, 30)
        pygame.draw.rect(self.surface, color,
                         rect_border, border)

        border = (not self.downbeat_quarter_indicator) * 1

        rect_border = pygame.Rect(478, 10, 30, 30)
        pygame.draw.rect(self.surface, color,
                         rect_border, border)

    def update_control(self):
        """ Overriding GUISurface.update_control()
        """
        self.needs_rendering = False
        if tto_globals.midi and tto_globals.midi.transport_new_messages:
            self.needs_rendering = True
            tto_globals.midi.transport_new_messages = False

            if tto_globals.midi.downbeat_whole:
                self.downbeat_whole_indicator = not \
                    self.downbeat_whole_indicator

            if tto_globals.midi.downbeat_half:
                self.downbeat_half_indicator = not \
                    self.downbeat_half_indicator

            if tto_globals.midi.downbeat_quarter:
                self.downbeat_quarter_indicator = not \
                    self.downbeat_quarter_indicator
