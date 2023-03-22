from machine import Pin, UART
from time import sleep
from elm327 import ELM327
from lcd import LCD, colour
import math
from shift_light import SHIFT_LIGHT
from gauges import CIRCULAR_GAUGE, NUMERICAL_GAUGE


# init status LED (on-board LED on the Raspberry Pi Pico)
led = Pin(25, Pin.OUT)
led.value(0)

# init UART (connector is GND TX RX VDD)
serial = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

# init ELM327 (OBD reader)
# print("Resetting ELM327...")
# elm = ELM327(serial)
# elm.reset()
# print("ELM reset done!")

# init display
# print("Resetting LCD...")
# lcd = LCD()
# lcd.fill(colour(0, 0, 0))  # BLACK
# lcd.show()
# print("LCD reset done!")

# init buttons
keyA = Pin(15, Pin.IN, Pin.PULL_UP)  # Normally 1 but 0 if pressed
keyB = Pin(17, Pin.IN, Pin.PULL_UP)
keyX = Pin(19, Pin.IN, Pin.PULL_UP)
keyY = Pin(21, Pin.IN, Pin.PULL_UP)

up = Pin(2, Pin.IN, Pin.PULL_UP)
down = Pin(18, Pin.IN, Pin.PULL_UP)
left = Pin(16, Pin.IN, Pin.PULL_UP)
right = Pin(20, Pin.IN, Pin.PULL_UP)
ctrl = Pin(3, Pin.IN, Pin.PULL_UP)

voltage = None
speed = None
rpm = None
pressure = None
default_color = colour(255, 0, 0)

shift_light = SHIFT_LIGHT(
    pixel_count=8,
    segments_count=8,
    pin=4,
    base_colour=(55, 0, 0),
    limiter_colour=(0, 0, 200),
    minimum_rpm=4000,
    maximum_rpm=6500,
)
#
# circular_gauge = CIRCULAR_GAUGE(
#     scale_colour=(128, 128, 128),
#     needle_colour=(250, 0, 0),
#     value_colour=(250, 0, 0),
#     text_colour=(128, 128, 128),
#     parameter_name="TEST",
#     parameter_units="V",
# )
# circular_gauge.display_base()
# circular_gauge.update_display(
#     value=12.7,
#     min_value=0,
#     max_value=15,
#     parameter_name="TEST",
#     parameter_units="V",
# )
sleep(0.5)
# numerical_gauge = NUMERICAL_GAUGE(
#     value_colour=(255, 0, 0),
#     text_colour=(128, 128, 128),
#     parameter_name="TEST",
#     parameter_units="V",
# )
# numerical_gauge.display_base()
# numerical_gauge.update_display(min_value=0,max_value=15,value=12.7)

while True:
    print(keyA.value())
    if keyA.value() == 0:
        print("Key A pressed")
    if keyB.value() == 0:
        print("Key B pressed")
    if keyX.value() == 0:
        print("Key X pressed")
    if keyY.value() == 0:
        print("Key Y pressed")

    if up.value() == 0:
        print("Key up pressed")
        circular_gauge = CIRCULAR_GAUGE(
            scale_colour=(128, 128, 128),
            needle_colour=(250, 0, 0),
            value_colour=(250, 0, 0),
            text_colour=(128, 128, 128),
            parameter_name="TEST",
            parameter_units="V",
        )
        circular_gauge.display_base()
    if down.value() == 0:
        print("Key down pressed")
        numerical_gauge = NUMERICAL_GAUGE(
            value_colour=(255, 0, 0),
            text_colour=(128, 128, 128),
            parameter_name="TEST",
            parameter_units="V",
        )
        numerical_gauge.display_base()
    if left.value() == 0:
        print("Key left pressed")
    if right.value() == 0:
        print("Key right pressed")
    if ctrl.value() == 0:
        print("Key ctrl pressed")
    sleep(0.1)
    # for n in range(0,6500,5):
    #    shift_light.display_rpm(n)
    # print(n)
    # sleep(0.1)
    # circular_gauge.update_display(value=1)
    # numerical_gauge.update_display()
    # toggle led for good measure (crash indicator)
    # led.toggle()
    # sleep(1)
    ##
    # try:
    #    voltage = elm.read_battery_voltage()
    #    speed = int(elm.get_speed())
    # rpm = int(elm.get_engine_rpm())
    # print("RPM:   ", rpm)
    #    pressure = int(elm.get_intake_manifold_pressure())
    ##
    # except Exception:
    # print("Data not recieved!")
    # sleep(0.1)

    # sleep(0.25)
    # rpm = 4500
    # shift_light.display_rpm(rpm)

    # lcd.fill(colour(0, 0, 0))
    # # sleep(0.01)
    # lcd.printstring(f"VOLTAGE", 55, 10, 3, 0, 0, colour(220, 220, 220))
    # # for n in range(10):
    # #    lcd.ring(100,150,70+n,default_color)
    # lcd.fill_rect(85, 75, 90, 90, colour(0, 0, 0))
    # for n in range(3):
    #     lcd.ring(85, 120, 70 - n, colour(128, 128, 128))
    # lcd.fill_rect(85, 120, 240, 240, colour(0, 0, 0))
    # lcd.vline(85, 190, 20, colour(128, 128, 128))
    # lcd.hline(155, 120, 15, colour(128, 128, 128))
    # # lcd.line(65, 95, 50, 100, colour(128, 128, 128))
    # lcd.printstring("0V", 75, 210, 2, 0, 0, default_color)
    # # lcd.printstring("7.5V", 65, 95, 1, 0, 0, default_color)
    # lcd.printstring("15V", 175, 113, 2, 0, 0, default_color)
    # # lcd.printstring("12.4V", 135, 180, 3, 0, 0, colour(220, 220, 220))
    # # pointer line, valid angle range is 0-270
    # for k in range(0, 271, 5):

    #     value = round((k * 15 / 271), 1)
    #     print(value)
    #     angle = k
    #     radius = 65
    #     center_point_x = 85
    #     center_point_y = 120
    #     edge_point_x = 0
    #     edge_point_y = 0
    #     y_coord = int(radius * math.sin(math.radians(angle)))
    #     x_coord = int(radius * math.cos(math.radians(angle)))

    #     if angle >= 0 and angle <= 90:
    #         edge_point_x = center_point_x - y_coord
    #         edge_point_y = center_point_y + x_coord
    #     if angle > 90 and angle <= 180:
    #         edge_point_x = center_point_x - y_coord
    #         edge_point_y = center_point_y + x_coord
    #     if angle > 180 and angle <= 270:
    #         edge_point_x = center_point_x - y_coord
    #         edge_point_y = center_point_y + x_coord

    #     lcd.line(
    #         center_point_x,
    #         center_point_y,
    #         edge_point_x,
    #         edge_point_y,
    #         colour(255, 0, 0),
    #     )
    #     lcd.line(
    #         center_point_x + 2,
    #         center_point_y,
    #         edge_point_x,
    #         edge_point_y,
    #         colour(255, 0, 0),
    #     )
    #     lcd.line(
    #         center_point_x - 2,
    #         center_point_y,
    #         edge_point_x,
    #         edge_point_y,
    #         colour(255, 0, 0),
    #     )

    #     # clearing needle
    #     needle_x_coords = [
    #         center_point_x,
    #         center_point_x + 2,
    #         center_point_x - 2,
    #         edge_point_x,
    #     ]
    #     needle_y_coords = [
    #         center_point_y,
    #         center_point_y + 2,
    #         center_point_y - 2,
    #         edge_point_y,
    #     ]
    #     blank_rectangle_x_len = max(needle_x_coords) - min(needle_x_coords)
    #     blank_rectangle_y_len = max(needle_y_coords) - min(needle_y_coords)

    #     string_value = str(value)
    #     print(int(string_value[0]))
    #     if value < 10:

    #         lcd.seg(
    #             115, 160, int(string_value[0]), 6, colour(0, 0, 0), colour(0, 0, 0)
    #         )  # blank segment
    #         lcd.seg(
    #             135, 160, int(string_value[0]), 6, colour(0, 0, 0), colour(255, 0, 0)
    #         )
    #         # dot is not a valid digit
    #         lcd.seg(
    #             185, 160, int(string_value[2]), 6, colour(0, 0, 0), colour(255, 0, 0)
    #         )
    #     else:
    #         lcd.seg(
    #             95, 160, int(string_value[0]), 6, colour(0, 0, 0), colour(255, 0, 0)
    #         )
    #         lcd.seg(
    #             135, 160, int(string_value[1]), 6, colour(0, 0, 0), colour(255, 0, 0)
    #         )
    #         # dot is not a valid digit
    #         lcd.seg(
    #             185, 160, int(string_value[3]), 6, colour(0, 0, 0), colour(255, 0, 0)
    #         )
    #     lcd.fill_rect(170, 205, 10, 10, colour(255, 0, 0))
    #     lcd.show()
    #     lcd.fill_rect(
    #         blank_rectangle_min_x,
    #         blank_rectangle_min_y,
    #         blank_rectangle_x_len + 1,
    #         blank_rectangle_y_len + 1,
    #         colour(0, 0, 0),
    #     )
    # if voltage:
    #     # print("Voltage:     ", voltage.split()[1])

    #     if len(voltage.split()[1]) != 5:
    #         lcd.fill_rect(25, 120, 40, 40, colour(0, 0, 0))
    #     else:
    #         lcd.printstring(f"{voltage.split()[1]}", 25, 120, 3, 0, 0, default_color)

    # # print("Pressure:    ", pressure)
