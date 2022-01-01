import tto_fonts
import tto_globals
import pygame


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
