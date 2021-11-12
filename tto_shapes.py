import math
import tto_globals


class Shape(object):
    def __init__(self, **kwargs):
        # Informal interface for Shape

        # coordinate lists used by find_coordinates and render methods:
        # If the shape is a polygon, line etc represented by a list of
        #   coordinate pairs:
        self.coordinates = []  # [(x, y), (x, y), ...]
        # If the shape has some rotation associated with each coordinate
        #   pair e.g. for placing and rotating text labels at each
        #   location:
        self.degrees = []  # [0, 90, 180, ...]
        # If the shape represents rectangles, which pycharm expects
        #   in (x, y, w, h):
        self.coordinates_boxes = []  # [(x, y, w, h), ...]

        self.canvas_size = kwargs.get('canvas_size', 100)

        # Polar coordinate system values for circles, etc:
        self.r = kwargs.get('r', 0)  # Radius, default 0px
        # Center of the canvas X
        self.origin_x = int(self.canvas_size / 2) + tto_globals.canvas_margin
        # Center of the canvas Y
        self.origin_y = int(self.canvas_size / 2) + tto_globals.canvas_margin
        self.circle_divisions = 12  # 12-slices around the circle
        # slice_no for specifying a pizza-like division of a circle
        self.slice_no = kwargs.get('slice_no', 1)
        # offset_orientation is a number of degrees added to everything
        # to set an overall coordinate system rotation/orientation
        self.offset_orientation = 90
        # offset_degrees for tracking a # of degrees shape rotation
        self.offset_degrees = kwargs.get('offset_degrees', 0)

        # Spacing and margins for list shapes
        self.spacing_width = kwargs.get('spacing_width', 0)
        self.line_spacing = kwargs.get('line_spacing', 0)
        self.left_margin = kwargs.get('left_margin', 0)

        self.find_coordinates()

    def find_coordinates(self):
        pass


class ShapeNotesList(Shape):
    def find_coordinates(self):
        for i in range(1, 13):
            self.coordinates.append(
                (
                    tto_globals.canvas_margin + self.left_margin +
                    (i * self.spacing_width),
                    tto_globals.canvas_margin + self.spacing_width +
                    self.line_spacing
                )
            )
            self.degrees.append(0)
            self.coordinates_boxes.append(
                (
                    tto_globals.canvas_margin +
                    (i * self.spacing_width) - int(self.spacing_width/2) +
                    self.left_margin,
                    tto_globals.canvas_margin +
                    self.spacing_width - int(self.spacing_width/2) +
                    self.line_spacing,
                    self.spacing_width,  # width
                    self.spacing_width   # height
                )
            )


class ShapeWheel(Shape):
    def find_coordinates(self):
        for i in range(12):
            self.coordinates.append(
                # One corner of the triangle along the circle radius r,
                # at sliceNo*1/12circle
                (
                    (
                        self.origin_x -
                        int(self.r * math.cos(
                            math.radians(
                                ((360 / self.circle_divisions) * i)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    ),
                    (
                        self.origin_y -
                        int(self.r * math.sin(
                            math.radians(
                                ((360 / self.circle_divisions) * i)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    )
                )
            )
            self.degrees.append(
                int(-((360 / self.circle_divisions) * i))
                - self.offset_degrees
            )


class ShapeWheelSlice(Shape):
    def find_coordinates(self):
        self.coordinates.append(  # Origin
            (
                self.origin_x,
                self.origin_y
            )
        )
        self.coordinates.append(
            # One corner of the triangle along the circle radius r,
            # at sliceNo*1/12circle
            (
                (
                    self.origin_x -
                    int(self.r * math.cos(
                        math.radians(
                            ((360 / self.circle_divisions) *
                             self.slice_no) + self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                ),
                (
                    self.origin_y -
                    int(self.r * math.sin(
                        math.radians(
                            ((360 / self.circle_divisions) *
                             self.slice_no) + self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                )
            )
        )
        self.coordinates.append(
            # One corner of the triangle along the circle radius r,
            # at (sliceNo+1)*1/12circle
            (
                (
                    self.origin_x -
                    int(self.r * math.cos(
                        math.radians(
                            ((360 / self.circle_divisions) * (
                                        self.slice_no + 1)) +
                            self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                ),
                (
                    self.origin_y -
                    int(self.r * math.sin(
                        math.radians(
                            ((360 / self.circle_divisions) * (
                                        self.slice_no + 1)) +
                            self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                )
            )
        )
        self.degrees.append(
            int(-((360 / self.circle_divisions) * self.slice_no))
            - self.offset_degrees
        )


class ShapeWheelRay(Shape):
    def find_coordinates(self):
        self.coordinates.append(  # Origin
            (
                self.origin_x,
                self.origin_y
            )
        )
        self.coordinates.append(
                (
                    (
                        self.origin_x -
                        int(self.r * math.cos(
                            math.radians(
                                ((360 / self.circle_divisions) * self.slice_no)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    ),
                    (
                        self.origin_y -
                        int(self.r * math.sin(
                            math.radians(
                                ((360 / self.circle_divisions) * self.slice_no)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    )
                )
            )
        self.degrees.append(
            int(-((360 / self.circle_divisions) * self.slice_no))
            - self.offset_degrees
        )
