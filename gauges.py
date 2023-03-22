from lcd import LCD
from constant import *
from lcd_utils import colour
import math


class CIRCULAR_GAUGE:
    def __init__(
        self,
        lcd: LCD,
        scale_colour: tuple[int, int, int],
        needle_colour: tuple[int, int, int],
        value_colour: tuple[int, int, int],
        text_colour: tuple[int, int, int],
        parameter_name: str = "PARAMETER",
        parameter_units: str = "UNITS",
    ):
        self.lcd = lcd
        self.scale_colour = scale_colour
        self.needle_colour = needle_colour
        self.value_colour = value_colour
        self.text_colour = text_colour
        self.parameter_name = parameter_name
        self.parameter_units = parameter_units
        self.value = 0
        self.min_value = 0
        self.max_value = 999
        self.needle_rectangle_coords = (0, 0, 0, 0)
        self.blank_needles_parameters = 3 * [(0, 0, 0, 0, colour(0, 0, 0))]
        self.lcd.fill(colour(0, 0, 0))

    def update_range_min(self, min_value):
        self.min_value = min_value

    def update_range_max(self, max_value):
        self.max_value = max_value

    def update_value(self, value):
        if value > self.max_value:
            value = self.max_value
        if value < self.min_value:
            value = self.min_value
        self.value = value

    def update_parameter_name(self, parameter_name):
        self.parameter_name = parameter_name

    def update_parameter_units(self, parameter_units):
        self.parameter_units = parameter_units

    def update_display(
        self,
        value=None,
        min_value=None,
        max_value=None,
        parameter_name=None,
        parameter_units=None,
    ):
        if min_value is not None:
            self.update_range_min(min_value)
            self.display_base()
        if max_value is not None:
            self.update_range_max(max_value)
            self.display_base()
        if parameter_name is not None:
            self.update_parameter_name(parameter_name)
            self.display_base()
        if parameter_units is not None:
            self.update_parameter_units(parameter_units)
            self.display_base()
        if value is not None and value != self.value:
            self.update_value(value)
            self.display_values()

    def display_base(self):
        """Function for displaying the background"""
        self.lcd.fill(colour(0, 0, 0))
        self.lcd.printstring(
            (self.parameter_name + " " + self.parameter_units),
            45,
            10,
            3,
            0,
            0,
            colour(*self.text_colour),
        )
        for n in range(3):
            self.lcd.ring(85, 120, 70 - n, colour(*self.scale_colour))
        self.lcd.fill_rect(85, 120, 240, 240, colour(0, 0, 0))
        self.lcd.vline(85, 190, 20, colour(*self.scale_colour))
        self.lcd.hline(155, 120, 15, colour(*self.scale_colour))
        self.lcd.printstring(
            (str(self.min_value)),
            30,
            210,
            2,
            0,
            0,
            colour(*self.scale_colour),
        )
        self.lcd.printstring(
            (str(self.max_value)),
            175,
            113,
            2,
            0,
            0,
            colour(*self.scale_colour),
        )
        self.lcd.show()

    def display_values(self):
        """Function for displaying actual reading"""
        self.draw_value()
        self.draw_needle()
        self.lcd.show()
        for line in self.blank_needles_parameters:
            self.lcd.line(*line)

    def draw_needle(self):
        """Function for drawing the needle"""
        radius = 65
        center_point_x = 85
        center_point_y = 120
        edge_point_x = 0
        edge_point_y = 0
        angle = self.needle_angle

        y_coord = int(radius * math.sin(math.radians(angle)))
        x_coord = int(radius * math.cos(math.radians(angle)))

        if angle >= 0 and angle <= 90:
            edge_point_x = center_point_x - y_coord
            edge_point_y = center_point_y + x_coord
        if angle > 90 and angle <= 180:
            edge_point_x = center_point_x - y_coord
            edge_point_y = center_point_y + x_coord
        if angle > 180 and angle <= 270:
            edge_point_x = center_point_x - y_coord
            edge_point_y = center_point_y + x_coord

        self.lcd.line(
            center_point_x,
            center_point_y,
            edge_point_x,
            edge_point_y,
            colour(*self.needle_colour),
        )
        self.lcd.line(
            center_point_x + 2,
            center_point_y,
            edge_point_x,
            edge_point_y,
            colour(*self.needle_colour),
        )
        self.lcd.line(
            center_point_x - 2,
            center_point_y,
            edge_point_x,
            edge_point_y,
            colour(*self.needle_colour),
        )

        needles_start_coords = [center_point_x, center_point_x + 2, center_point_x - 2]

        self.blank_needles_parameters = self.calculate_blank_needles_parameters(
            needles_start_coords, center_point_y, edge_point_x, edge_point_y
        )

    @property
    def needle_angle(self):
        angle = round(
            (abs(self.value - self.min_value) / abs(self.max_value - self.min_value))
            * 270,
            1,
        )
        return angle

    def calculate_blank_needles_parameters(
        self, needles_start_coords, center_point_y, edge_point_x, edge_point_y
    ):
        blank_needles = []
        for coord in needles_start_coords:
            blank_needles.append(
                (coord, center_point_y, edge_point_x, edge_point_y, colour(0, 0, 0))
            )
        return blank_needles

    def draw_value(self):
        """Function for displaying numerical parameter value"""
        self.lcd.fill_rect(95, 160, 100, 100, colour(0, 0, 0))
        string_value = str(float(abs(self.value)))
        value_type = self.value_type
        if value_type == "decimal":
            if abs(self.value) < 10:
                self.lcd.seg(
                    110,
                    160,
                    int(string_value[0]),
                    6,
                    colour(0, 0, 0),
                    colour(0, 0, 0),
                )  # blank segment
                self.lcd.seg(
                    150,
                    160,
                    int(string_value[0]),
                    6,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
                # dot is not a valid digit
                self.lcd.seg(
                    200,
                    160,
                    int(string_value[2]),
                    6,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
            else:
                self.lcd.seg(
                    110,
                    160,
                    int(string_value[0]),
                    6,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
                self.lcd.seg(
                    150,
                    160,
                    int(string_value[1]),
                    6,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
                # dot is not a valid digit
                self.lcd.seg(
                    200,
                    160,
                    int(string_value[3]),
                    6,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
            if self.value < 0:
                self.lcd.fill_rect(95, 185, 15, 5, colour(*self.value_colour))
            self.lcd.fill_rect(185, 205, 10, 10, colour(*self.value_colour))
        if value_type == "non_decimal":
            string_value = str(int(abs(self.value)))
            # Padding to 3 digits
            if len(string_value) == 1:
                string_value = "xx" + string_value
            if len(string_value) == 2:
                string_value = "x" + string_value

            if string_value[0] != "x":
                self.lcd.seg(
                    115,
                    160,
                    int(string_value[0]),
                    6,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
            else:
                self.lcd.seg(
                    115,
                    160,
                    int("0"),
                    6,
                    colour(0, 0, 0),
                    colour(0, 0, 0),
                )
            if string_value[1] != "x":
                self.lcd.seg(
                    155,
                    160,
                    int(string_value[1]),
                    6,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
            else:
                self.lcd.seg(
                    155,
                    160,
                    int("0"),
                    6,
                    colour(0, 0, 0),
                    colour(0, 0, 0),
                )
            self.lcd.seg(
                195,
                160,
                int(string_value[2]),
                6,
                colour(0, 0, 0),
                colour(*self.value_colour),
            )
            if self.value < 0:
                self.lcd.fill_rect(95, 185, 15, 5, colour(*self.value_colour))

    @property
    def value_type(self):
        if (self.max_value - self.min_value) < 100:
            return "decimal"
        else:
            return "non_decimal"


class NUMERICAL_GAUGE:
    def __init__(
        self,
        lcd: LCD,
        value_colour: tuple[int, int, int],
        text_colour: tuple[int, int, int],
        parameter_name: str = "PARAMETER",
        parameter_units: str = "UNITS",
    ):
        self.lcd = lcd
        self.value_colour = value_colour
        self.text_colour = text_colour
        self.parameter_name = parameter_name
        self.parameter_units = parameter_units
        self.value = 0
        self.min_value = 0
        self.max_value = 9999
        self.scale_factor = 9
        self.spacing_width = 10
        self.digit_width = 45
        self.negative_symbol_width = 30
        self.negative_symbol_height = 15
        self.dot_dimension = 15
        self.dot_y_offset = 70
        self.y_offset = 60

        self.lcd.fill(colour(0, 0, 0))

    def update_range_min(self, min_value):
        self.min_value = min_value

    def update_range_max(self, max_value):
        self.max_value = max_value

    def update_value(self, value):
        self.value = value

    def update_parameter_name(self, parameter_name):
        self.parameter_name = parameter_name

    def update_parameter_units(self, parameter_units):
        self.parameter_units = parameter_units

    def update_display(
        self,
        value=None,
        min_value=None,
        max_value=None,
        parameter_name=None,
        parameter_units=None,
    ):
        if min_value is not None:
            self.update_range_min(min_value)
            self.display_base()
        if max_value is not None:
            self.update_range_max(max_value)
            self.display_base()
        if parameter_name is not None:
            self.update_parameter_name(parameter_name)
            self.display_base()
        if parameter_units is not None:
            self.update_parameter_units(parameter_units)
            self.display_base()
        if value is not None:
            self.update_value(value)
            self.display_values()

    def display_base(self):
        """Function for displaying the background"""
        self.lcd.fill(colour(0, 0, 0))
        self.lcd.printstring(
            (self.parameter_name + " " + self.parameter_units),
            45,
            10,
            3,
            0,
            0,
            colour(*self.text_colour),
        )

        self.lcd.show()

    def display_values(self):
        """Function for displaying actual reading"""
        self.draw_value()
        self.lcd.show()

    def draw_value(self):
        """Function for displaying numerical parameter value"""
        self.lcd.fill_rect(0, 60, 240, 120, colour(0, 0, 0))
        number_of_symbols = 0
        value_type = self.value_type
        string_value = ""
        if value_type == "decimal" and abs(self.value) < 10:
            string_value = "{:.2f}".format(abs(self.value))
        if value_type == "decimal" and abs(self.value) >= 10:
            string_value = "{:.1f}".format(abs(self.value))
        if value_type == "non_decimal":
            string_value = "{:.0f}".format(abs(self.value))

        splitted_string_value = string_value.split(".")

        if len(splitted_string_value) == 1:  # we have an intiger value
            number_of_symbols = len(string_value)
            number_box_width = (
                number_of_symbols * self.digit_width
                + (number_of_symbols - 1) * self.spacing_width
            )
        else:  # we have a floating point value
            for item in splitted_string_value:
                number_of_symbols += len(item)
            number_box_width = (
                number_of_symbols * self.digit_width
                + (number_of_symbols - 1) * self.spacing_width
            )
            number_box_width += 2 * self.spacing_width + self.dot_dimension

        number_box_x_min = int((WIDTH - number_box_width) / 2)

        if self.is_value_negative:
            self.lcd.fill_rect(
                5,
                int(self.dot_y_offset / 2) + self.y_offset,
                self.negative_symbol_width,
                self.negative_symbol_height,
                colour(*self.value_colour),
            )
            number_box_x_min += self.negative_symbol_width

        for n, symbol in enumerate(string_value):
            symbol_x_offset = (
                n * (self.spacing_width + self.digit_width) + number_box_x_min
            )
            if symbol != ".":
                if "." in string_value[:n]:
                    symbol_x_offset -= self.digit_width - self.dot_dimension
                self.lcd.seg(
                    symbol_x_offset,
                    self.y_offset,
                    int(symbol),
                    9,
                    colour(0, 0, 0),
                    colour(*self.value_colour),
                )
            else:
                self.lcd.fill_rect(
                    symbol_x_offset,
                    self.y_offset + self.dot_y_offset,
                    self.dot_dimension,
                    self.dot_dimension,
                    colour(*self.value_colour),
                )

    @property
    def value_type(self):
        if (self.max_value - self.min_value) < 100:
            return "decimal"
        else:
            return "non_decimal"

    @property
    def is_value_negative(self):
        if self.value < 0:
            return True
        else:
            return False
