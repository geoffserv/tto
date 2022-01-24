from tto_pygame_guisurface import GUISurface
import tto_globals
from tto_shapes import *
import pygame


class GUISurfaceKeyboardMap(GUISurface):
    def __init__(self, canvas_width, canvas_height, blit_x, blit_y, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(canvas_width, canvas_height,
                                             blit_x, blit_y, **kwargs)

        self.keyboard_cols = 12
        self.keyboard_rows = 4

        # keyboard_layout is a list of lists,
        # keyboard_layout[] represents each row
        # keyboard_layout[][] is the cols
        # within which is a dict representing the key, labels, actions, etc
        # Initialize a default layout
        self.keyboard_layout = []
        for row in range(self.keyboard_rows):
            self.keyboard_layout.append([])
            for col in range(self.keyboard_cols):
                self.keyboard_layout[row].append(
                    {
                        'keyboard_code': 0,
                        'setting': "",
                        'value': 0,
                        'button_label_default': "",
                        'button_label_1': "",
                        'button_label_2': "",
                        'button_label_3': "",
                        'button_color_bg': tto_globals.color_black,
                        'button_color_bg_default': tto_globals.color_black,
                        'button_color_bg_on': tto_globals.color_orange_50,
                        'button_color_fg': tto_globals.color_orange_50,
                        'button_color_fg_default': tto_globals.color_orange_50
                    }
                )

        # Set-up row 1
        # Key signature / Tone class / Tonal root
        i = 0
        # Set button labels
        for button_default_label in ('C', 'G', 'D', 'A', 'E', 'B',
                                     'Gb', 'Db', 'Ab', 'Eb', 'Bb',
                                     'F'):
            self.keyboard_layout[0][i][
                'button_label_default'] = button_default_label
            self.keyboard_layout[0][i]['button_label_1'] = button_default_label
            i += 1

        # Set button actions and action values
        i = 0
        for button_value in range(12):
            self.keyboard_layout[0][i]['value'] = button_value
            self.keyboard_layout[0][i]['setting'] = "key"
            i += 1

        i = 0
        #                              bg_color   , fg_color
        for button_default_colors in ((tto_globals.color_white,
                                       tto_globals.color_black),  # C
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # G
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # D
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # A
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # E
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # B
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # Gb
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # Db
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # Ab
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # Eb
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # Bb
                                      (tto_globals.color_white,
                                       tto_globals.color_black)):  # F
            self.keyboard_layout[0][i]['button_color_bg'] = \
                button_default_colors[0]
            self.keyboard_layout[0][i]['button_color_bg_default'] = \
                button_default_colors[0]
            self.keyboard_layout[0][i]['button_color_fg'] = \
                button_default_colors[1]
            self.keyboard_layout[0][i]['button_color_fg_default'] = \
                button_default_colors[1]
            i += 1

        # Set-up row 2
        # Set button labels
        i = 0
        for button_default_label in (1, 5, 2, 6, 3, 7, 4, 1, 5, 2, 6, 3):
            self.keyboard_layout[1][i][
                'button_label_default'] = button_default_label
            self.keyboard_layout[1][i]['button_label_1'] = button_default_label
            i += 1

        # Set button actions and values
        i = 0
        for button_value in (0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4):
            self.keyboard_layout[1][i]['value'] = button_value
            self.keyboard_layout[1][i]['setting'] = "scale"
            i += 1

        i = 0
        #                              bg_color   , fg_color
        for button_default_colors in ((tto_globals.color_white,
                                       tto_globals.color_black),  # 1
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 5
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 2
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 6
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 3
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 7
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 4
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 1
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 5
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 2
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 6
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50)):  # 3
            self.keyboard_layout[1][i]['button_color_bg'] = \
                button_default_colors[0]
            self.keyboard_layout[1][i]['button_color_bg_default'] = \
                button_default_colors[0]
            self.keyboard_layout[1][i]['button_color_fg'] = \
                button_default_colors[1]
            self.keyboard_layout[1][i]['button_color_fg_default'] = \
                button_default_colors[1]
            i += 1

        # Set-up row 3
        i = 0
        for button_default_label in (1, 5, 2, 6, 3, 7, 4, 1, 5, 2, 6, 3):
            self.keyboard_layout[2][i]['button_label_default'] = \
                button_default_label
            self.keyboard_layout[2][i]['button_label_1'] = \
                button_default_label
            i += 1

        i = 0
        for button_value in (0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4):
            self.keyboard_layout[2][i]['value'] = button_value
            self.keyboard_layout[2][i]['setting'] = "chord"
            i += 1

        i = 0
        #                              bg_color   , fg_color
        for button_default_colors in ((tto_globals.color_white,
                                       tto_globals.color_black),  # 1
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 5
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 2
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 6
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 3
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 7
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 4
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 1
                                      (tto_globals.color_white,
                                       tto_globals.color_black),  # 5
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 2
                                      (tto_globals.color_black,
                                       tto_globals.color_orange_50),  # 6
                                      (tto_globals.color_white,
                                       tto_globals.color_black)):  # 3
            self.keyboard_layout[2][i]['button_color_bg'] = \
                button_default_colors[0]
            self.keyboard_layout[2][i]['button_color_bg_default'] = \
                button_default_colors[0]
            self.keyboard_layout[2][i]['button_color_fg'] = \
                button_default_colors[1]
            self.keyboard_layout[2][i]['button_color_fg_default'] = \
                button_default_colors[1]
            i += 1

        # Set-up row 4
        i = 0
        for button_default_label in range(12):
            self.keyboard_layout[3][i]['button_label_default'] = 'fn'
            self.keyboard_layout[3][i]['button_label_1'] = 'fn'
            self.keyboard_layout[3][i]['button_color_bg'] = \
                tto_globals.color_white
            self.keyboard_layout[3][i]['button_color_bg_default'] = \
                tto_globals.color_white
            self.keyboard_layout[3][i]['button_color_fg'] = \
                tto_globals.color_black
            self.keyboard_layout[3][i]['button_color_fg_default'] = \
                tto_globals.color_black
            i += 1

        self.button_keyboard_codelist = \
            (96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45,
             113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93,
             97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 13,
             1073742049,  # left shift key code
             122, 120, 99, 118, 98, 110, 109, 44, 46, 47, 1073742053  # r shft
             )

        # button_keyboard_codes is indexed against the keyboard code and
        # contains
        # a tuple of where within keyboard_layout that button's attributes
        # are found.
        # Useful for associating a keyboard event with the keyboard_layout
        # options
        # related to that button in a GUISurface update_control() etc
        self.button_keyboard_codes = {}
        i = 0
        for row in range(self.keyboard_rows):
            for col in range(self.keyboard_cols):
                self.button_keyboard_codes[
                    self.button_keyboard_codelist[i]] = \
                    (row, col)
                i += 1

        self.cols = self.keyboard_cols
        self.rows = self.keyboard_rows

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
                                 self.keyboard_layout[row][col]
                                 ['button_color_bg'],
                                 rect_key,
                                 0)
                # Foreground square border
                rect_key = pygame.Rect(110 + (col * 70),
                                       10 + (row * 70),
                                       60,
                                       60)
                pygame.draw.rect(self.surface,
                                 self.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                 rect_key,
                                 1)
                # Per-button label 1 - 5 char width
                self.draw_label(coordinates=(110 + (col * 70) + 4,
                                             10 + (row * 70) ),
                                degrees=0,
                                text_label="{}".format(
                                    self.keyboard_layout[row][col]
                                    ['button_label_1']),
                                font=self.font,
                                color=self.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                align="left")
                # Per-button label 2 - 5 char width
                self.draw_label(coordinates=(110 + (col * 70) + 4,
                                             10 + (row * 70)  + 20),
                                degrees=0,
                                text_label="{}".format(
                                    self.keyboard_layout[row][col]
                                    ['button_label_2']),
                                font=self.font,
                                color=self.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                align="left")
                # Per-button label 3 - 5 char width
                self.draw_label(coordinates=(110 + (col * 70) + 4,
                                             10 + (row * 70) + 40),
                                degrees=0,
                                text_label="{}".format(
                                    self.keyboard_layout[row][col]
                                    ['button_label_3']),
                                font=self.font,
                                color=self.keyboard_layout[row][col]
                                 ['button_color_fg'],
                                align="left")

    def update_control_invert_button_colors(self, row, col):
        # Flip-flop foreground and background colors for the button boxes
        # for whenever a button is pushed / released
        if (self.keyboard_layout[row][col]['button_color_bg'] ==
           self.keyboard_layout[row][col]['button_color_bg_default']):
            self.keyboard_layout[row][col]['button_color_bg'] = \
                self.keyboard_layout[row][col]['button_color_bg_on']
            self.keyboard_layout[row][col]['button_color_fg'] = \
                self.keyboard_layout[row][col]['button_color_bg_default']
        else:
            self.keyboard_layout[row][col]['button_color_fg'] = \
                self.keyboard_layout[row][col]['button_color_fg_default']
            self.keyboard_layout[row][col]['button_color_bg'] = \
                self.keyboard_layout[row][col]['button_color_bg_default']

    def update_control(self):
        """ Overriding GUISurface.update_control()
        """
        self.needs_rendering = False
        for event in tto_globals.events:
            tto_globals.debugger.message(
                "KEYB",
                "GUISurfaceKeyboardMap update_control() saw event: {}".format(
                    event))

            if tto_globals.events[event]['type'] == "KD":
                # Seeing a KeyDown event
                if tto_globals.events[event]['keycode'] in \
                        self.button_keyboard_codes:
                    # We know about it.  Time to action

                    row = self.button_keyboard_codes[
                            tto_globals.events[event]['keycode']][0]  # row

                    col = self.button_keyboard_codes[
                            tto_globals.events[event]['keycode']][1]  # col

                    # Turn 'on' the visual button
                    self.update_control_invert_button_colors(row, col)
                    self.needs_rendering = True

                    if self.keyboard_layout[row][col]['setting'] == "key":
                        tto_globals.debugger.message(
                            "KEYB",
                            "Row {} Col {} KB down - Key to {}".format(
                                row,
                                col,
                                self.keyboard_layout[row][col]['value']
                            )
                        )

                        tto_globals.key.current_key = \
                            self.keyboard_layout[row][col]['value']

                    if self.keyboard_layout[row][col]['setting'] == "scale":
                        tto_globals.debugger.message(
                            "KEYB",
                            "Row {} Col {} KB down - Scale to {}".format(
                                row,
                                col,
                                self.keyboard_layout[row][col]['value']
                            )
                        )

                        tto_globals.key.current_scale_degree = \
                            self.keyboard_layout[row][col]['value']

                    if self.keyboard_layout[row][col]['setting'] == "chord":
                        tto_globals.debugger.message(
                            "KEYB",
                            "Row {} Col {} KB down - Chord to {}".format(
                                row,
                                col,
                                self.keyboard_layout[row][col]['value']
                            )
                        )

            if tto_globals.events[event]['type'] == "KU":
                # Seeing a KeyUp event
                if tto_globals.events[event]['keycode'] in \
                        self.button_keyboard_codes:
                    # We know about it.  action

                    row = self.button_keyboard_codes[
                              tto_globals.events[event]['keycode']][0]  # row

                    col = self.button_keyboard_codes[
                        tto_globals.events[event]['keycode']][1]  # col

                    # Turn 'off' the visual button
                    self.update_control_invert_button_colors(row, col)

                    self.needs_rendering = True
                    