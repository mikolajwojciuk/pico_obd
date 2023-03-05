from machine import Pin, UART
from time import sleep
from elm327 import ELM327


# init status LED (on-board LED on the Raspberry Pi Pico)
led = Pin(25, Pin.OUT)
led.value(0)

# init UART (connector is GND TX RX VDD)
serial = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

# init ELM327 (OBD reader)
print("Resetting ELM327...")
elm = ELM327(serial)
elm.reset()
print("ELM reset done!")

voltage = None


while True:
    # toggle led for good measure (crash indicator)
    led.toggle()
    sleep(1)

    try:
        # speed = int(elm.get_speed())
        # rpm = int(elm.get_engine_rpm())
        # pressure = int(elm.get_intake_manifold_pressure())
        voltage = elm.read_battery_voltage()

    except Exception:
        print("Data not recieved!")
        sleep(0.5)

    print("Voltage:         ", voltage)
