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

        # These are used to track rotation animation of the wheel
        # rotate_steps tracks how many remaining frames of rotation are left
        # to animate for key wheel rotation
        # rotate_iterator will be 1 or -1, and is added to rotate_offset once
        # per cycle until rotate_steps runs out
        self.rotate_steps = 0
        self.rotate_iterator = 0

        # These are used to track rotation animation of the note selection
        # rotate_steps_note tracks how many remaining frames of rotation are
        # left to animate for note selection
        # rotate_iterator_note, same as above but for note selection
        self.rotate_steps_chord = 0
        self.rotate_iterator_chord = 0

        # rotate_amount is how many degrees to hop per event
        # 1 degree per event makes turning the circle sloooow
        self.rotate_amount = int(360 / 36)
        # rotate_speedup is a multiplier of frames to skip, to make
        # animation super quick.  Factors of 30 will work best
        self.rotate_speedup = 10

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

    def set_wheel(self, set_index):
        self.needs_rendering = True
        self.rotate_offset = int(set_index * (360/12))

    def rotate_wheel(self, direction):
        # Set direction to 1 for clockwise rotation
        # Set direction to -1 for counterclockwise rotation
        # It's an integer of degrees added to the overall rotation
        # If this is called and there is no rotation currently, begin
        #   rotation immediately
        if (self.rotate_steps == 0) or (self.rotate_iterator != direction):
            self.rotate_steps = int(self.rotate_amount / self.rotate_speedup) \
                                - self.rotate_steps
            self.rotate_iterator = direction

            print("self.rotate_offset:", self.rotate_offset,
                  "rotate_offset + rotate_amount:",
                  self.rotate_offset +
                  (self.rotate_amount * self.rotate_iterator),
                  "mod 360/12:",
                  (self.rotate_offset +
                   (self.rotate_iterator * self.rotate_amount)) % (360 / 12),
                  "self.rotate_amount:", self.rotate_amount,
                  "self.rotate_iterator:", self.rotate_iterator)

            # Edge detection around the wheel
            # With the current rotate_amount (360/36),
            # If the rotation iterator is 1 and the abs value of the rotation
            #   amt mod (360/12) reaches 20, time to rotate the key.
            # If the rotation iterator is -1 and the abs value of the rotation
            #   amt mod (360/12) reaches 10, time to rotate as well.
            if ((self.rotate_iterator == 1) and
                (abs((self.rotate_offset +
                      (self.rotate_amount * self.rotate_iterator))
                     % (360 / 12)) == 20)) or \
                    ((self.rotate_iterator == -1) and
                     (abs((self.rotate_offset +
                           (self.rotate_amount * self.rotate_iterator))
                          % (360 / 12)) == 10)):
                # Set the key index as we turn around
                # Subtract because of the rotating-disk mechanic, the chosen
                # option is OPPOSITE direction of the disk turning
                tto_globals.key.rotate_key(add_by=(-1*self.rotate_iterator))

                # Change the chord, too
                tto_globals.key.rotate_chord(add_by=(-1*self.rotate_iterator))

    def rotate_chord(self, direction):
        # Set direction to 1 for clockwise rotation
        # Set direction to -1 for counterclockwise rotation
        # It's an integer of degrees added to the overall rotation
        # If this is called and there is no rotation currently, begin
        #   rotation immediately

        if (self.rotate_steps_chord == 0) or \
                (self.rotate_iterator_chord != direction):
            self.rotate_steps_chord = int(self.rotate_amount /
                                          self.rotate_speedup) \
                                      - self.rotate_steps_chord
            self.rotate_iterator_chord = direction

            if ((self.rotate_iterator_chord == 1) and
                (abs((self.rotate_offset_chord +
                      (self.rotate_amount * self.rotate_iterator_chord))
                     % (360 / 12)) == 20)) or \
                    ((self.rotate_iterator_chord == -1) and
                     (abs((self.rotate_offset_chord +
                           (self.rotate_amount * self.rotate_iterator_chord))
                          % (360 / 12)) == 10)):

                # Change the mode
                tto_globals.key.rotate_key_mode(
                    add_by=self.rotate_iterator_chord)

                if (abs((tto_globals.key.current_chord_root -
                         tto_globals.key.current_key) % 12) <= 5) or \
                        (abs((tto_globals.key.current_chord_root -
                              tto_globals.key.current_key) % 12) == 11):
                    # Change the chord
                    tto_globals.key.rotate_chord(
                        add_by=self.rotate_iterator_chord)

                # Handle the "rollover" as the pointer skips past non-Diotonics
                # if helm_globals.chord_position == 6:
                if abs((tto_globals.key.current_chord_root -
                        tto_globals.key.current_key) % 12) == 6:
                    tto_globals.key.rotate_chord(set_to=(11 + tto_globals.
                                                         key.current_key))
                    self.rotate_offset_chord += 150

                if abs((tto_globals.key.current_chord_root -
                        tto_globals.key.current_key) % 12) == 10:
                    tto_globals.key.rotate_chord(set_to=(5 + tto_globals.
                                                         key.current_key))
                    self.rotate_offset_chord -= 150

    def update_control(self):
        self.needs_rendering = False
        # Handle the dict of events passed in for this update
        for event in tto_globals.events:

            pass

            # if 'trigger_note' in tto_globals.events[event] and \
            #         tto_globals.events[event]['trigger_note']:
            #     notes_effected = tto_globals.key.calculate_chord(
            #         tto_globals.chord_definitions[tto_globals.events[event]['chord']])
            #     if 'start' in tto_globals.events[event] and tto_globals.events[event]['start']:
            #         self.needs_rendering = True
            #         tto_globals.midi.notes_trigger(mode="on",
            #                                         notes=notes_effected)
            #         tto_globals.midi.notes_prior = notes_effected
            #     if 'stop' in tto_globals.events[event] and tto_globals.events[event]['stop']:
            #         self.needs_rendering = True
            #         # Turn off the currently selected notes, plus the prior
            #         # fired notes:
            #         notes_effected.extend(tto_globals.midi.notes_prior)
            #         tto_globals.midi.notes_trigger(mode="off",
            #                                         notes=notes_effected)

            # if 'rotate' in tto_globals.events[event] and \
            #         tto_globals.events[event]['rotate']:
            #     if tto_globals.events[event]['wheel'] == "key":
            #         if tto_globals.events[event]['dir'] == "cw":
            #             self.rotate_wheel(1)
            #         if tto_globals.events[event]['dir'] == "ccw":
            #             self.rotate_wheel(-1)
            #     if tto_globals.events[event]['wheel'] == "chord":
            #         if tto_globals.events[event]['dir'] == "cw":
            #             self.rotate_chord(1)
            #         if tto_globals.events[event]['dir'] == "ccw":
            #             self.rotate_chord(-1)

        # Perform any animation steps needed for this update
        if self.rotate_steps > 0:
            self.needs_rendering = True
            self.rotate_offset += (self.rotate_iterator * self.rotate_speedup)
            self.rotate_steps -= 1

        if self.rotate_steps_chord > 0:
            self.needs_rendering = True
            self.rotate_offset_chord += (self.rotate_iterator_chord *
                                         self.rotate_speedup)
            self.rotate_steps_chord -= 1

    def draw_control(self):

        ####################
        # Background stuff #
        ####################

        self.surface.fill(self.color_bg)

        self.draw_control_border()

        # Key label
        for i in [0]:  # Wheel position 0
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r-7,
                                    slice_no=i)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "Key",
                            tto_fonts.font['medium'],
                            self.color)

        # Labels for directions
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

        # Draw the reference circle
        # This uses self.rotate_offset, so it's a rotating layer
        label_circle = ShapeWheel(canvas_size=self.r * 2,
                                  r=self.r - 56,
                                  offset_degrees=self.rotate_offset)
        self.draw_key_labels(label_circle, tto_globals.key.notes)

        # Draw the slices
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

        for i in range(12):
            # "Currently playing" highlights, if on:
            if ((i + tto_globals.key.current_key) % 12) \
                    in tto_globals.key.notes_on:
                polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                          r=self.r - 160,
                                          slice_no=i,
                                          offset_degrees=self.offset_degrees)
                self.draw_polygon(polygon, 0, self.color)

        for label in tto_globals.note_wheel_labels:
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 200,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["step"]),
                            tto_fonts.font['medium_bold'],
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 240,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(tto_globals.note_wheel_labels[label]
                                ["triad"]),
                            tto_fonts.font['small_bold'],
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 365,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0] + 90,
                            str(tto_globals.note_wheel_labels[label]
                                ["mode"]),
                            tto_fonts.font['small_bold'],
                            self.color_bg)

        # Draw the selected note indicator
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 126,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "↑",
                        tto_fonts.font['x_large'],
                        self.color)