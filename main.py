from time import sleep
from machine import Pin, UART

# initialize UART
serial = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

from elm327 import ELM327

# initialize ELM327 (OBD reader)
elm = ELM327(serial)
elm.reset()
elm.search_protocol()
from lcd import LCD, colour

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

from time import sleep
from shift_light import SHIFT_LIGHT
from gauges import CIRCULAR_GAUGE, NUMERICAL_GAUGE
import ujson

# init buttons
# keyA = Pin(15, Pin.IN, Pin.PULL_UP)  # Normally 1 but 0 if pressed
# keyB = Pin(17, Pin.IN, Pin.PULL_UP)
# keyX = Pin(19, Pin.IN, Pin.PULL_UP)
# keyY = Pin(21, Pin.IN, Pin.PULL_UP)
up = Pin(2, Pin.IN, Pin.PULL_UP)
down = Pin(18, Pin.IN, Pin.PULL_UP)
left = Pin(16, Pin.IN, Pin.PULL_UP)
right = Pin(20, Pin.IN, Pin.PULL_UP)
# ctrl = Pin(3, Pin.IN, Pin.PULL_UP)

# parameter - function dict
param_function = {
    "RPM": elm.get_engine_rpm,
    "Coolant": elm.get_engine_coolant_temperature,
    "IMP": elm.get_intake_manifold_pressure,
    "Speed": elm.get_speed,
    "Oil temp.": elm.get_engine_oil_temperature,
    "Voltage": elm.read_battery_voltage,
    "STFT": elm.get_stft,
    "LTFT": elm.get_ltft,
    "IAT": elm.get_intake_air_temp,
    "Timing advance": elm.get_timing_advance,
    "Throttle": elm.get_throttle_position,
    "Fuel level": elm.get_fuel_level,
}

# replace with None for init
param_values = {
    "RPM": 0,
    "Coolant": 0,
    "IMP": 0,
    "Speed": 0,
    "Oil temp.": 0,
    "Voltage": 0,
    "STFT": 0,
    "LTFT": 0,
    "IAT": 0,
    "Timing advance": 0,
    "Throttle": 0,
    "Fuel level": 0,
}
with open("config.json", "r") as config_file:
    config = ujson.load(config_file)


shift_light = SHIFT_LIGHT(
    pixel_count=8,
    segments_count=8,
    pin=4,
    base_colour=(55, 0, 0),
    limiter_colour=(0, 0, 200),
    minimum_rpm=2000,
    maximum_rpm=3000,
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


numerical_gauge = NUMERICAL_GAUGE(
    lcd,
    value_colour=(255, 0, 0),
    text_colour=(128, 128, 128),
    parameter_name="Voltage",
    parameter_units="V",
)


numerical_gauge.display_base()
numerical_gauge.update_display(min_value=0, max_value=15)

show_default_parameter = True
default_color = colour(255, 0, 0)
parameter_switch_counter = 0
parameter_index = 0
current_gauge = numerical_gauge
# circular_gauge.display_base()


parameters_list = [parameter["parameter_name"] for parameter in config["PARAMETERS"]]

current_parameter_name = parameters_list[parameter_index]

while True:
    # get the rpm
    try:
        rpm = elm.get_engine_rpm()
    except:
        rpm = 0
    shift_light.display_rpm(rpm)

    try:
        param_values[current_parameter_name] = param_function[current_parameter_name]()
    except:
        param_values[current_parameter_name] = 0

    value = param_values[current_parameter_name]
    current_parameter_index = parameter_index

    if left.value() == 0:
        parameter_switch_counter -= 1
    if right.value() == 0:
        parameter_switch_counter += 1

    parameter_index = parameter_switch_counter % len(config["PARAMETERS"])
    current_parameter_name = parameters_list[parameter_index]

    if current_parameter_index != parameter_index:
        parameter = config["PARAMETERS"][parameter_index]
        current_gauge.update_display(
            value=value,
            min_value=parameter["min_value"],
            max_value=parameter["max_value"],
            parameter_units=parameter["units"],
            parameter_name=parameter["parameter_name"],
        )
    elif show_default_parameter:
        parameter = config["PARAMETERS"][parameter_index]
        current_gauge.update_display(
            value=value,
            min_value=parameter["min_value"],
            max_value=parameter["max_value"],
            parameter_units=parameter["units"],
            parameter_name=parameter["parameter_name"],
        )
        show_default_parameter = False
    else:
        current_gauge.update_display(value=value)

    if up.value() == 0:
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
