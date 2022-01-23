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

        self.rotate_offset = int(tto_globals.key.current_key * (-360/12))

        # For the Chord Interval labels, rollover from position 6 to 11
        # because all the non-Diatonics live in positions 6-10
        adjusted_scale_degree = tto_globals.key.current_scale_degree
        if adjusted_scale_degree == 6:
            adjusted_scale_degree = 11

        self.rotate_offset_chord = int(adjusted_scale_degree *
                                       (360/12))

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

        # Scale Degree word label
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 100,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "Scale degree",
                        tto_fonts.font['small_bold'],
                        self.color_bg)

        # Scale Degree number & labels all the way around the wheel
        for label in tto_globals.note_wheel_labels:
            # The actual digit label
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 130,
                                    slice_no=label)

            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["step"]),
                            tto_fonts.font['medium_bold'],
                            self.color_bg)

            # The triad e.g. MAJ, min, dim
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 160,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["triad"]),
                            tto_fonts.font['small_bold'],
                            self.color_bg)

            # The scale degree mode e.g. Ionian, Mixolydian, etc
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 180,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["mode"]),
                            tto_fonts.font['x_small'],
                            self.color_bg)

        #########################################
        # Selected scale degree chord intervals #
        #########################################

        # The up arrow ↑
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 213,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "↑",
                        tto_fonts.font['large_bold'],
                        self.color_bg)

        # The chord interval words
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 247,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "Chord",
                        tto_fonts.font['x_small'],
                        self.color_bg)
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 263,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "interval",
                        tto_fonts.font['x_small'],
                        self.color_bg)

        # The 'slices' of tto_globals.note_wheel_labels in the default order
        scale_degree_order = [11, 0, 1, 2, 3, 4, 5]

        # Now Cut The Deck depending on tto_globals.key.current_scale_degree
        if tto_globals.key.current_scale_degree > 0:
            scale_degree_order = \
                scale_degree_order[7-tto_globals.key.current_scale_degree:] + \
                scale_degree_order[0:7-tto_globals.key.current_scale_degree]

        # Chord interval number all the way around the wheel
        for label in tto_globals.note_wheel_labels:
            # The actual digit label
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 295,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[
                                    scale_degree_order.pop(0)
                                ]
                                ["step"]),
                            tto_fonts.font['medium_bold'],
                            self.color_bg)
