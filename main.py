from machine import Pin, UART
from time import sleep
from elm327 import ELM327
from lcd import LCD, colour
import math
import random
from shift_light import SHIFT_LIGHT
from gauges import CIRCULAR_GAUGE, NUMERICAL_GAUGE
from constant import *

# init status LED (on-board LED on the Raspberry Pi Pico)
led = Pin(25, Pin.OUT)
led.value(0)

# init UART (connector is GND TX RX VDD)
serial = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

# init ELM327 (OBD reader)
#print("Resetting ELM327...")
#elm = ELM327(serial)
#elm.reset()
#print("ELM reset done!")

# init display
print("Resetting LCD...")
lcd = LCD(
    BL,
    DC,
    RST,
    MOSI,
    SCK,
    CS,
    WIDTH,
    HEIGHT,
    SPI_ID,
    SPI_BAUDRATE,
    SPI_POLARITY,
    SPI_PHASE,
    DISPLAY_RED,
    DISPLAY_GREEN,
    DISPLAY_BLUE,
    DISPLAY_WHITE,
)
lcd.fill(colour(0, 0, 0))  # BLACK
lcd.show()
print("LCD reset done!")

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


rpm = 0
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
circular_gauge = CIRCULAR_GAUGE(
    lcd,
    scale_colour=(128, 128, 128),
    needle_colour=(250, 0, 0),
    value_colour=(250, 0, 0),
    text_colour=(128, 128, 128),
    parameter_name="RPM",
    parameter_units="",
)
circular_gauge.display_base()
circular_gauge.update_display(
    min_value=0,
    max_value=7000,
    parameter_name="RPM",
    parameter_units="",
)
# sleep(5)
numerical_gauge = NUMERICAL_GAUGE(
    lcd,
    value_colour=(255, 0, 0),
    text_colour=(128, 128, 128),
    parameter_name="RPM",
    parameter_units="",
)
numerical_gauge.display_base()
numerical_gauge.update_display(min_value=0, max_value=7000)


current_gauge = circular_gauge
circular_gauge.display_base()

while True:
    
    rpm += 50
    sleep(0.1)
#     try:
#         rpm = int(elm.get_engine_rpm())
#     except:
#         print("Data not recieved!")

    value = rpm
    current_gauge.update_display(value=value)
    shift_light.display_rpm(rpm)

    if up.value() == 0:
        print("Key up pressed")
        lcd.fill(colour(0, 0, 0))  # BLACK
        lcd.show()
        circular_gauge.display_base()
        circular_gauge.update_display(value=value)
        current_gauge = circular_gauge

    if down.value() == 0:
        print("Key down pressed")
        lcd.fill(colour(0, 0, 0))  # BLACK
        lcd.show()
        # numerical_gauge.display_base()
        numerical_gauge.update_display(min_value=0, max_value=7000, value=value)
        current_gauge = numerical_gauge
