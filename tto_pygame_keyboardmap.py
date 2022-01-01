from tto_pygame_guisurface import GUISurface
import tto_globals
from tto_shapes import *
import pygame


class GUISurfaceKeyboardMap(GUISurface):
    def __init__(self, canvas_width, canvas_height, blit_x, blit_y, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(canvas_width, canvas_height,
                                             blit_x, blit_y, **kwargs)

        self.cols = tto_globals.keyboard_cols
        self.rows = tto_globals.keyboard_rows

        self.color = tto_globals.color_orange_50

    def draw_control(self):
        """ Overriding GUISurface.draw_control()
        """
        self.surface.fill(self.color_bg)
        self.draw_control_border()

        # Draw the keyboard row labels
        self.draw_label(coordinates=(8, 7),
                        degrees=0,
                        text_label="Key sig",
                        font=self.font,
                        color=self.color,
                        align="left")
        self.draw_label(coordinates=(8, 27),
                        degrees=0,
                        text_label="Tone class",
                        font=self.font,
                        color=self.color,
                        align="left")
        self.draw_label(coordinates=(8, 47),
                        degrees=0,
                        text_label="Tonal root",
                        font=self.font,
                        color=self.color,
                        align="left")

        self.draw_label(coordinates=(8, 27 + 71 - 10),
                        degrees=0,
                        text_label="Scale",
                        font=self.font,
                        color=self.color,
                        align="left")
        self.draw_label(coordinates=(8, 27 + 71 + 10),
                        degrees=0,
                        text_label="degree",
                        font=self.font,
                        color=self.color,
                        align="left")

        self.draw_label(coordinates=(8, 27 + (71 * 2) - 10),
                        degrees=0,
                        text_label="Chord",
                        font=self.font,
                        color=self.color,
                        align="left")
        self.draw_label(coordinates=(8, 27 + (71 * 2) + 10),
                        degrees=0,
                        text_label="interval",
                        font=self.font,
                        color=self.color,
                        align="left")

        self.draw_label(coordinates=(8, 27 + (71 * 3) - 10),
                        degrees=0,
                        text_label="Control",
                        font=self.font,
                        color=self.color,
                        align="left")
        self.draw_label(coordinates=(8, 27 + (71 * 3) + 10),
                        degrees=0,
                        text_label="buttons",
                        font=self.font,
                        color=self.color,
                        align="left")

        # Draw the keyboard
        for row in range(self.rows):
            for col in range(self.cols):
                # Background square color
                rect_key = pygame.Rect(110 + (col * 70),
                                       10 + (row * 70),
                                       60,
                                       60)
                pygame.draw.rect(self.surface,
                                 tto_globals.keyboard_layout[row][col]
                                 ['button_color_bg'],
                                 rect_key,
                                 0)
                # Foreground square border
                rect_key = pygame.Rect(110 + (col * 70),
                                       10 + (row * 70),
                                       60,
                                       60)
                pygame.draw.rect(self.surface,
                                 tto_globals.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                 rect_key,
                                 1)
                # Per-button label 1 - 5 char width
                self.draw_label(coordinates=(110 + (col * 70) + 4,
                                             10 + (row * 70) ),
                                degrees=0,
                                text_label="{}".format(
                                    tto_globals.keyboard_layout[row][col]
                                    ['button_label_1']),
                                font=self.font,
                                color=tto_globals.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                align="left")
                # Per-button label 2 - 5 char width
                self.draw_label(coordinates=(110 + (col * 70) + 4,
                                             10 + (row * 70)  + 20),
                                degrees=0,
                                text_label="{}".format(
                                    tto_globals.keyboard_layout[row][col]
                                    ['button_label_2']),
                                font=self.font,
                                color=tto_globals.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                align="left")
                # Per-button label 3 - 5 char width
                self.draw_label(coordinates=(110 + (col * 70) + 4,
                                             10 + (row * 70) + 40),
                                degrees=0,
                                text_label="{}".format(
                                    tto_globals.keyboard_layout[row][col]
                                    ['button_label_3']),
                                font=self.font,
                                color=tto_globals.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                align="left")

    def update_control_invert_button_colors(self, row, col):
        # Flip-flop foreground and background colors for the button boxes
        # for whenever a button is pushed / released
        if (tto_globals.keyboard_layout[row][col]['button_color_bg'] ==
           tto_globals.keyboard_layout[row][col]['button_color_bg_default']):
            tto_globals.keyboard_layout[row][col]['button_color_bg'] = \
                tto_globals.keyboard_layout[row][col]\
                ['button_color_bg_on']
            tto_globals.keyboard_layout[row][col]['button_color_fg'] = \
                tto_globals.keyboard_layout[row][col]\
                ['button_color_bg_default']
        else:
            tto_globals.keyboard_layout[row][col]['button_color_fg'] = \
                tto_globals.keyboard_layout[row][col]\
                ['button_color_fg_default']
            tto_globals.keyboard_layout[row][col]['button_color_bg'] = \
                tto_globals.keyboard_layout[row][col]\
                ['button_color_bg_default']

    def update_control(self):
        """ Overriding GUISurface.update_control()
        """
        self.needs_rendering = False
        for event in tto_globals.events:
            tto_globals.debugger.message(
                "PYGA",
                "GUISurfaceKeyboardMap update_control() saw event: {}".format(
                    event))

            if tto_globals.events[event]['type'] == "KD":
                # Seeing a KeyDown event
                # Turn 'on' the visual button
                if tto_globals.events[event]['keycode'] in \
                        tto_globals.button_keyboard_codes:
                    self.update_control_invert_button_colors(
                        tto_globals.button_keyboard_codes[
                            tto_globals.events[event]['keycode']][0],  # row
                        tto_globals.button_keyboard_codes[
                            tto_globals.events[event]['keycode']][1]  # col
                    )
                    self.needs_rendering = True

            if tto_globals.events[event]['type'] == "KU":
                # Seeing a KeyUp event
                # Turn 'off' the visual button
                if tto_globals.events[event]['keycode'] in \
                        tto_globals.button_keyboard_codes:
                    self.update_control_invert_button_colors(
                        tto_globals.button_keyboard_codes[
                            tto_globals.events[event]['keycode']][0],  # row
                        tto_globals.button_keyboard_codes[
                            tto_globals.events[event]['keycode']][1]  # col
                    )
                    self.needs_rendering = True