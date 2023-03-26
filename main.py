from machine import Pin, UART
from time import sleep
from elm327 import ELM327
from lcd import LCD, colour
from shift_light import SHIFT_LIGHT
from gauges import CIRCULAR_GAUGE, NUMERICAL_GAUGE
import ujson


# initialize UART
serial = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))
print("UART initialized!")

# initialize ELM327 (OBD reader)
#elm = ELM327(serial)
# elm.reset()
print("ELM327 initialized!")


# initialize display
lcd = LCD(
    13,
    8,
    12,
    11,
    10,
    9,
    240,
    240,
    1,
    100000_000,
    0,
    0,
    0x07E0,
    0x001F,
    0xF800,
    0xFFFF,
)

lcd.fill(colour(0, 0, 0))
lcd.show()
print("LCD initialized!")

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
print("Buttons initialized!")

with open("config.json", "r") as config_file:
    config = ujson.load(config_file)

print(config)

# Mock up values for testing
rpm = 2137
coolant = 87
imp = 123
speed = 91
oil_temp = 58
voltage = 14.4


test_values = [rpm, coolant, imp, speed, oil_temp, voltage]


default_color = colour(255, 0, 0)
parameter_switch_counter = 0
parameter_index = 0


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

# circular_gauge.display_base()

# circular_gauge.update_display(
#     min_value=0,
#     max_value=15,
#     parameter_name="RPM",
#     parameter_units="",
# )

numerical_gauge = NUMERICAL_GAUGE(
    lcd,
    value_colour=(255, 0, 0),
    text_colour=(128, 128, 128),
    parameter_name="RPM",
    parameter_units="",
)

# numerical_gauge.display_base()

# numerical_gauge.update_display(min_value=0, max_value=15)


current_gauge = numerical_gauge
# circular_gauge.display_base()

print(config["PARAMETERS"])
n = 0
while n < 5000:
    n += 1

    sleep(0.1)

    try:
        #    rpm = int(elm.get_engine_rpm())
        voltage = elm.read_battery_voltage()
        voltage = float(voltage.split("\r")[1][:-1])

    except:
        print("Data not recieved!")

    value = test_values[parameter_index]
    current_parameter_index = parameter_index

    shift_light.display_rpm(value)

    if left.value() == 0:
        parameter_switch_counter -= 1
    if right.value() == 0:
        parameter_switch_counter += 1

    parameter_index = parameter_switch_counter % len(config["PARAMETERS"])

    if current_parameter_index != parameter_index:
        parameter = config["PARAMETERS"][parameter_index]
        current_gauge.update_display(
            value=value,
            min_value=parameter["min_value"],
            max_value=parameter["max_value"],
            parameter_units=parameter["units"],
            parameter_name=parameter["parameter_name"],
        )
    else:
        current_gauge.update_display(value=value)

    if up.value() == 0:
        # lcd.fill(colour(0, 0, 0))  # BLACK
        # lcd.show()
        circular_gauge.display_base()
        parameter = config["PARAMETERS"][parameter_index]
        circular_gauge.update_display(
            value=value,
            min_value=parameter["min_value"],
            max_value=parameter["max_value"],
            parameter_units=parameter["units"],
            parameter_name=parameter["parameter_name"],
        )
        current_gauge = circular_gauge

    if down.value() == 0:
        # lcd.fill(colour(0, 0, 0))  # BLACK
        # lcd.show()
        numerical_gauge.display_base()
        parameter = config["PARAMETERS"][parameter_index]
        numerical_gauge.update_display(
            value=value,
            min_value=parameter["min_value"],
            max_value=parameter["max_value"],
            parameter_units=parameter["units"],
            parameter_name=parameter["parameter_name"],
        )
        current_gauge = numerical_gauge
