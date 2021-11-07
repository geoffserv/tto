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

        self.fps = 120  # Poll/Render no faster than this many fps
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

    def handle_pygame(self):
        """Non-blocking method to handle all pygame internals at a safe
        framerate.  Call this from the program main run loop.
        """
        if (time.time() - self.fps_tick) > self.fps_sec_per_frame:
            self.handle_input()
            self.handle_graphics()
            self.fps_tick = time.time()

    def handle_graphics(self):
        if self.canvas:
            # Check if any gui_surface reports that it needs rendering
            needs_rendering = False
            for gui_surface in self.gui_surfaces:
                if gui_surface.needs_rendering:
                    needs_rendering = True

            if needs_rendering:
                # First, flood the screen:
                self.canvas.fill(tto_globals.color_black)

                # Loop through each gui_surface added to the gui_surfaces
                for gui_surface in self.gui_surfaces:
                    # The drawControl method should update the control's visual
                    # elements and
                    # draw to the control's surface
                    gui_surface.draw_control()
                    # Blit the control's surface to the canvas
                    self.canvas.blit(gui_surface.surface,
                                     [gui_surface.blit_x,
                                      gui_surface.blit_y])
                pygame.display.update()

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
        # Only examine KEYDOWNs and KEYUPs:
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            tto_globals.debugger.message("PYGA",
                                         "Detected pygame.event: {}".
                                         format(event))


class GUISurface(object):
    def __init__(self, **kwargs):
        # Informal interface for a GUISurface

        # 100px x 100px canvas ratio default
        self.canvas_width = kwargs.get('canvas_size', 100)
        self.canvas_height = kwargs.get('canvas_size', 100)

        self.color = kwargs.get('color', tto_globals.color_orange)
        self.color_bg = kwargs.get('color_bg', tto_globals.color_black)
        self.color_accent = kwargs.get('color_accent',
                                       tto_globals.color_orange_25)

        # The X location in which this entire control
        # should be blit to the screen canvas
        self.blit_x = kwargs.get('blit_x', tto_globals.canvas_margin)

        # The Y location in which this entire control
        # should be blit to the screen canvas
        self.blit_y = kwargs.get('blit_y', tto_globals.canvas_margin)

        self.surface = None
        self.surface = pygame.Surface(
            (int(self.canvas_width + (tto_globals.canvas_margin * 2)),
             int(self.canvas_height + (tto_globals.canvas_margin * 2))))

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
                   color):
        text = font.render(text_label, False, color)
        text = pygame.transform.rotate(text, degrees)
        text_x_center = int(text.get_width() / 2)
        text_y_center = int(text.get_height() / 2)
        # Bit on to the surface:
        self.surface.blit(text, [coordinates[0] - text_x_center,
                                 coordinates[1] - text_y_center])

    def draw_control(self):
        pass

    def update_control(self, events):
        self.needs_rendering = False
