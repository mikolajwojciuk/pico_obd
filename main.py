from machine import Pin, UART
from time import sleep
from elm327 import ELM327
from lcd import LCD, colour
import math


# init status LED (on-board LED on the Raspberry Pi Pico)
led = Pin(25, Pin.OUT)
led.value(0)

# init UART (connector is GND TX RX VDD)
serial = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

print("\r")
# init ELM327 (OBD reader)
print("Resetting ELM327...")
elm = ELM327(serial)
elm.reset()
print("ELM reset done!")

print("Resetting LCD...")
lcd = LCD()
lcd.fill(colour(0, 0, 0))  # BLACK
lcd.show()
print("LCD reset done!")

voltage = None
speed = None
rpm = None
pressure = None
default_color = colour(255, 0, 0)

while True:
    # toggle led for good measure (crash indicator)
    led.toggle()
    sleep(1)
    #
    try:
        voltage = elm.read_battery_voltage()
        speed = int(elm.get_speed())
        rpm = int(elm.get_engine_rpm())
        pressure = int(elm.get_intake_manifold_pressure())
    #
    except Exception:
        print("Data not recieved!")
        sleep(0.5)
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
