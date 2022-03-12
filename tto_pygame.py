"""tto_pygame - pygame interface handler for tto

This module handles pygame input and output graphics


Requirements
------------
tto_globals : Program-wide global variable module for tto.
tto_fonts : Pygame Sysfonts
tto_shapes : Class and methods for calculating polygons
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
import time
from pygame.locals import *
from tto_pygame_helm import GUISurfaceHelm
from tto_pygame_keyboardmap import GUISurfaceKeyboardMap
from tto_pygame_transportstrip import GUISurfaceTransportStrip
from tto_pygame_terminal import GUISurfaceTerminal


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

        self.fps = 60  # Poll/Render pygame no faster than this many fps
        self.fps_sec_per_frame = (1 / self.fps)
        self.fps_tick = time.time()  # Tracking time for fps here

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
        time_since_last_ui = (time.time() - self.fps_tick)
        if time_since_last_ui > self.fps_sec_per_frame:
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
        if self.canvas:
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
                                          blit_y=390)
        self.gui_surfaces.append(gui_terminal)

        # The transport strip showing MIDI clock info, play/stop, quant info
        gui_tstrip = GUISurfaceTransportStrip(canvas_width=950,
                                              canvas_height=50,
                                              blit_x=960,
                                              blit_y=320)
        self.gui_surfaces.append(gui_tstrip)

        # A keyboard map showing all keys, mappings, button status, actions
        # This module maps keyboard input to actions downstream
        gui_keyboard_map = GUISurfaceKeyboardMap(canvas_width=950,
                                                 canvas_height=290,
                                                 blit_x=960,
                                                 blit_y=10)
        self.gui_surfaces.append(gui_keyboard_map)

        # The control wheel developed as part of the Helm project
        gui_helm = GUISurfaceHelm(canvas_width=930,
                                  canvas_height=930,
                                  blit_x=10,
                                  blit_y=10)
        self.gui_surfaces.append(gui_helm)
