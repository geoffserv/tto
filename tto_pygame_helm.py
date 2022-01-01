from tto_pygame_guisurface import GUISurface
import tto_globals
import tto_fonts
from tto_shapes import *


class GUISurfaceHelm(GUISurface):
    def __init__(self, canvas_width, canvas_height, blit_x, blit_y, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(canvas_width, canvas_height,
                                             blit_x, blit_y, **kwargs)

        # Radius for polar coord system
        self.r = int(self.canvas_height / 2)

        # rotate_offset tracks the overall rotation of the wheel in degrees
        # As the user rotates the wheel, this value is incremented/decremented
        self.rotate_offset = 0

        # rotate_offset_note tracks overall rotation, but for the selected
        # note
        self.rotate_offset_chord = 0

        # The circle is divided in to 12 segments
        # But if want a _side_ to be oriented upwards, not a _point_
        # then back it up an additional 1/24th of a circle
        self.offset_degrees = int(-360 / 24)

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
                font = tto_fonts.font['medium_bold']
            else:
                font = tto_fonts.font['medium']
            self.draw_label(coordinates,
                            shape.degrees[coord_pair],
                            note_label,
                            font,
                            self.color)
            coord_pair += 1

    def update_control(self):
        self.needs_rendering = False
        # Handle the dict of events passed in for this update
        for event in tto_globals.events:
            pass

    def draw_control(self):

        ####################
        # Background stuff #
        ####################

        self.surface.fill(self.color_bg)

        self.draw_control_border()

        #############
        # Key label #
        #############

        for i in [0]:  # Wheel position 0
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r-7,
                                    slice_no=i)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "Key",
                            tto_fonts.font['medium'],
                            self.color)

        #########################
        # Labels for directions #
        #########################

        for i in [1]:  # Wheel position 1
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r-7,
                                    slice_no=i)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "5ths >",
                            tto_fonts.font['medium'],
                            self.color_accent)
        for i in [11]:  # Wheel position 11
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r-7,
                                    slice_no=i)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "< 4ths",
                            tto_fonts.font['medium'],
                            self.color_accent)

        ############################
        # Draw the key note labels #
        ############################
        # This uses self.rotate_offset, so it's a rotating layer
        label_circle = ShapeWheel(canvas_size=self.r * 2,
                                  r=self.r - 56,
                                  offset_degrees=self.rotate_offset)
        self.draw_key_labels(label_circle, tto_globals.key.notes)

        ############################
        # Draw the diatonic slices #
        ############################
        for i in [0, 1, 2, 3, 4, 5, 11]:
            # Inner triangles bg color fill
            polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                      r=self.r - 70,
                                      slice_no=i,
                                      offset_degrees=self.offset_degrees)
            self.draw_polygon(polygon, 0, self.color_accent)

            # Outlines
            polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                      r=self.r - 12,
                                      slice_no=i,
                                      offset_degrees=self.offset_degrees)
            self.draw_polygon(polygon, 1, self.color)

        ########################################
        # Highlight anything currently playing #
        ########################################
        for i in range(12):
            # "Currently playing" highlights, if on:
            if ((i + tto_globals.key.current_key) % 12) \
                    in tto_globals.key.notes_on:
                polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                          r=self.r - 160,
                                          slice_no=i,
                                          offset_degrees=self.offset_degrees)
                self.draw_polygon(polygon, 0, self.color)

        ###################
        # Diatonic labels #
        ###################
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 115,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "Scale degree",
                        tto_fonts.font['small_bold'],
                        self.color_bg)

        for label in tto_globals.note_wheel_labels:
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 155,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["step"]),
                            tto_fonts.font['medium_bold'],
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 195,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["triad"]),
                            tto_fonts.font['small_bold'],
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 217,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["mode"]),
                            tto_fonts.font['x_small'],
                            self.color_bg)

        ####################################
        # Draw the selected note indicator #
        ####################################
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 256,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "↑",
                        tto_fonts.font['x_large'],
                        self.color)