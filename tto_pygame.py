"""tto_pygame - pygame interface handler for tto

This module handles pygame input and output graphics


Requirements
------------
tto_globals : Program-wide global variable module for tto.
pygame : library for the development of multimedia applications
time : to calculate math around frame rate.

Classes
-------
TtoPygame : Pygame class for tto.

Functions
---------
pygame_terminate() : Gracefully terminate pygame.
"""

import tto_globals
import tto_fonts
import pygame
from pygame.locals import *
import time


def pygame_terminate():
    """Gracefully terminate pygame.

    This should try to handle any final cleanup and close any open resources
    used by pygame.
    """
    try:
        tto_globals.debugger.message("PYGA", "Quitting Pygame")
        pygame.quit()
    except Exception as e:
        tto_globals.debugger.message("EXCEPTION",
                                     "Error during pygame.quit(): {}".
                                     format(e))


class TtoPygame(object):
    def __init__(self):
        self.fullscreen = tto_globals.config['tto'].getboolean('FullScreen')
        self.canvas_width = tto_globals.config['tto'].getint('CanvasWidth')
        self.canvas_height = tto_globals.config['tto'].\
            getint('CanvasHeight')
        self.init_gfx = tto_globals.config['tto'].getboolean('GraphicsEnabled')

        self.canvas = None  # Gfx display will be attached here

        self.fps = 120  # Poll/Render pygame no faster than this many fps
        self.fps_sec_per_frame = (1 / self.fps)
        self.fps_tick = time.time()  # Tracking time for fps here

        self.r = int(
            (self.canvas_height * .8) / 2)  # R is half of __% of the screen

        try:
            tto_globals.debugger.message("PYGA", "Starting Pygame")

            # Only init the display and fonts.  Do not init pygame's sound.
            # mido is handling our midi.  We do not need pygame sound.
            # Measured about 10% improvement on main loop performance
            pygame.display.init()
            pygame.font.init()
            # pygame.mixer.init()  # Do not init

            # Set up global fonts for the program interface
            tto_fonts.init_fonts()

        except Exception as e:
            tto_globals.debugger.message("EXCEPTION",
                                         "Error during pygame init(): {}".
                                         format(e))
            tto_globals.debugger.exit("Could not pygame init().")

        if self.init_gfx:
            # If this is being run headless, turn initGfx to False
            # This is useful for headless CI testing
            if self.fullscreen:
                self.canvas = pygame.display.set_mode(
                    [self.canvas_width, self.canvas_height], pygame.NOFRAME)
                pygame.display.toggle_fullscreen()
                # Workaround for pygame.FULLSCREEN going blank in Ubuntu
            else:
                self.canvas = pygame.display.set_mode(
                    [self.canvas_width, self.canvas_height])
            pygame.display.set_caption('tto')  # Set the window title

        # gui_surfaces list contains each controlSystem object that is
        # rendered.
        # Declare GUISurface objects, set them up and init them,
        # then append() them
        # to this list.  Then each in turn will get a drawControl() call and
        # their surface attribute will be blit to the canvas.
        self.gui_surfaces = []

        self.init_gui_surfaces()

    def handle_pygame(self):
        """Non-blocking method to handle all pygame internals at a safe
        framerate.  Call this from the program main run loop.
        """
        if (time.time() - self.fps_tick) > self.fps_sec_per_frame:
            self.handle_graphics()
            self.handle_input()
            self.handle_updates()
            self.fps_tick = time.time()

    def handle_graphics(self):
        if self.canvas:
            # Check if any gui_surface reports that it needs rendering
            needs_rendering = False
            for gui_surface in self.gui_surfaces:
                if gui_surface.needs_rendering:
                    needs_rendering = True

            if needs_rendering:
                try:
                    # First, flood the screen:
                    self.canvas.fill(tto_globals.color_black)

                    # Loop through each gui_surface added to the gui_surfaces
                    for gui_surface in self.gui_surfaces:
                        # The drawControl method should update the control's
                        # visual elements and
                        # draw to the control's surface
                        gui_surface.draw_control()
                        # Blit the control's surface to the canvas
                        self.canvas.blit(gui_surface.surface,
                                         [gui_surface.blit_x,
                                          gui_surface.blit_y])
                    pygame.display.update()
                except Exception as e:
                    tto_globals.debugger.message("EXCEPTION",
                                                 "Error drawing pygame: {}".
                                                 format(e))
                    tto_globals.debugger.exit("Pygame render error.")

    def handle_updates(self):
        if self.canvas:
            for gui_surface in self.gui_surfaces:
                gui_surface.update_control()

    def handle_input(self):
        if self.canvas:
            # pygame.event.get() must be run regularly as part of the main
            # program run() loop, or else pygame goes unresponsive.

            # REMINDER that pygame.event.set_allowed is defined in the
            # class constructor and is limiting what will come through here:

            for event in pygame.event.get():

                # Program exit events:
                if event.type == QUIT:  # The GUI window 'close' button, etc:
                    tto_globals.running = False

                if event.type == pygame.KEYDOWN:  # ESC to quit
                    if event.key == pygame.K_ESCAPE:
                        tto_globals.running = False

                # Pass all events to the input_key handler
                self.handle_input_key(event)

    def handle_input_key(self, event):
        """Filter out KEY-based input signals and add to tto_globals.events
        """
        if event.type in (pygame.KEYUP, pygame.KEYDOWN):
            event_type = "NA"  # Unknown type
            if event.type == pygame.KEYUP:
                event_type = "KU"  # KeyUp
            if event.type == pygame.KEYDOWN:
                event_type = "KD"  # KeyDown

            event_label = "{}_{}".format(event_type, event.key)
            tto_globals.debugger.message("PYGA",
                                         "handle_input_key() detected: {}".
                                         format(event_label))
            tto_globals.events[event_label] = {'type': event_type,
                                               'keycode': event.key,
                                               'event': event}


    def init_gui_surfaces(self):
        """Set-up all GUI elements here, and append() each to gui_surfaces
        As part of the framerate-gated handle_graphics() execution, everything
        in gui_surfaces is iterated across and draw_control() /
        update_control() are called
        """

        # A Terminal that shows live updates to tto_globals.debugger.messages
        gui_terminal = GUISurfaceTerminal(canvas_width=950,
                                          canvas_height=260,
                                          blit_x=960,
                                          blit_y=810)
        self.gui_surfaces.append(gui_terminal)

        # The transport strip showing MIDI clock info, play/stop, quant info
        gui_tstrip = GUISurfaceTransportStrip(canvas_width=950,
                                              canvas_height=50,
                                              blit_x=960,
                                              blit_y=740)
        self.gui_surfaces.append(gui_tstrip)

        # A keyboard map showing all keys, mappings, button status, actions
        gui_keyboard_map = GUISurfaceKeyboardMap(canvas_width=950,
                                                 canvas_height=290,
                                                 blit_x=960,
                                                 blit_y=430)
        self.gui_surfaces.append(gui_keyboard_map)


class GUISurface(object):
    def __init__(self, canvas_width, canvas_height, blit_x, blit_y, **kwargs):
        # Informal interface for a GUISurface

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.color = kwargs.get('color', tto_globals.color_orange)
        self.color_bg = kwargs.get('color_bg', tto_globals.color_black)
        self.color_accent = kwargs.get('color_accent',
                                       tto_globals.color_orange_25)

        # This is a nice little default font
        self.font = tto_fonts.font['small_mono']

        # The X location in which this entire control
        # should be blit to the screen canvas
        self.blit_x = blit_x

        # The Y location in which this entire control
        # should be blit to the screen canvas
        self.blit_y = blit_y

        self.surface = None
        self.surface = pygame.Surface(
            (int(self.canvas_width + (tto_globals.canvas_margin * 2)),
             int(self.canvas_height + (tto_globals.canvas_margin * 2))))

        # self.needs_rendering:
        # If this is true for this GUI surface object, the screen will be
        # re-rendered on the next main loop run.
        # This will be set to False at the beginning of every execution of the
        #   update_control method.
        # Then, during execution of the update_control method, it will be set
        #   to True if some change is detected which requires a re-render.
        # As we come back around in the main loop, if True is detected here,
        # Everyone gets redrawn.
        # For now, set to True so we get an initial render.
        self.needs_rendering = True

    def init_surface(self):
        pass

    def draw_polygon(self, shape, width, color):
        pygame.draw.polygon(self.surface, color, shape.coordinates, width)

    def draw_key_labels(self, shape, labels):
        coord_pair = 0
        for coordinates in shape.coordinates:
            if (coord_pair >= tto_globals.key.current_key) and \
               (coord_pair <= (tto_globals.key.current_key + 5)) and \
                    (tto_globals.key.current_key in range(7)):
                # sharps
                note_label = labels[coord_pair]['sharpName']
            else:
                note_label = labels[coord_pair]['noteName']
            if tto_globals.key.current_key == coord_pair:
                font = tto_globals.font['medium_bold']
            else:
                font = tto_globals.font['medium']
            self.draw_label(coordinates,
                            shape.degrees[coord_pair],
                            note_label,
                            font,
                            self.color)
            coord_pair += 1

    def draw_label(self, coordinates, degrees, text_label, font,
                   color, align="center"):
        text = font.render(text_label, False, color)
        text = pygame.transform.rotate(text, degrees)

        text_x = 0
        text_y = 0

        if align == "center":
            text_x = int(text.get_width() / 2)
            text_y = int(text.get_height() / 2)

        # Bit on to the surface:
        self.surface.blit(text, [coordinates[0] - text_x,
                                 coordinates[1] - text_y])

    def draw_control_border(self):
        """ Draw a control border
        # Rect(left, top, width, height)
        """
        rect_border = pygame.Rect(0, 0, self.canvas_width, self.canvas_height)
        pygame.draw.rect(self.surface, tto_globals.color_orange_50,
                         rect_border, 2)

    def draw_control(self):
        """ Draw the actual GUI elements on self.surface
        Minimally, self.draw_control_border() for a uniform program-wide
        GUI surface border between various elements.
        """
        self.surface.fill(self.color_bg)
        self.draw_control_border()

    def update_control(self):
        """ Determines whether needs_rendering = True
        and can perform any necessary task for the GUI surface with access to
        the tto_globals.events dict
        Override as necessary.
        """
        self.needs_rendering = False


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
