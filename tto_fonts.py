"""tto_fonts - pygame graphic interface fonts for tto

This module handles pygame SysFonts.

Requirements
------------
tto_globals : Program-wide global variable module for tto.
pygame : library for the development of multimedia applications

Functions
---------
init_fonts() : call pygame.font.SysFont() to initialize each desired typeface
"""

import pygame
import tto_globals

font = {}  # Fonts used throughout the project stored here as a dict


def init_fonts():
    # Don't call this until after pygame.init() in the master module.
    global font
    #print(pygame.font.get_fonts())
    #exit()
    try:
        tto_globals.debugger.message("FONT", "Loading SysFonts")
        font = {'small': pygame.font.SysFont('sfnsmono', 16),
                'small_bold': pygame.font.SysFont('sfnsmono', 16, bold=True),
                'small_mono': pygame.font.SysFont('sfnsmono', 16),
                'medium': pygame.font.SysFont('sfnsmono', 24),
                'medium_bold': pygame.font.SysFont('sfnsmono', 24, bold=True),
                'x_large': pygame.font.SysFont('sfnsmono', 60)}
    except Exception as e:
        tto_globals.debugger.message("EXCEPTION",
                                     "Error loading SysFonts: {}".
                                     format(e))
        tto_globals.debugger.exit("Could not load fonts.")
