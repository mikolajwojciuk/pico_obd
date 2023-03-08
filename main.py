from machine import Pin, UART
from time import sleep
from elm327 import ELM327
from lcd import LCD_screen, colour


# init status LED (on-board LED on the Raspberry Pi Pico)
led = Pin(25, Pin.OUT)
led.value(0)

# init UART (connector is GND TX RX VDD)
serial = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

print("\r")
# init ELM327 (OBD reader)
print("Resetting ELM327...")
# elm = ELM327(serial)
# elm.reset()
print("ELM reset done!")

print("Resetting LCD...")
lcd = LCD_screen()
lcd.fill(colour(0, 0, 0))  # BLACK
lcd.show()
print("LCD reset done!")

voltage = None
default_color = colour(255, 0, 0)

while True:
    # toggle led for good measure (crash indicator)
    led.toggle()
    sleep(1)

    try:
        voltage = elm.read_battery_voltage()
        # speed = int(elm.get_speed())
        # rpm = int(elm.get_engine_rpm())
        # pressure = int(elm.get_intake_manifold_pressure())

    except Exception:
        print("Data not recieved!")
        sleep(0.5)

    lcd.printstring(f"Voltage", 55, 25, 3, 0, 0, colour(220, 220, 220))

    # for n in range(10):
    #    lcd.ring(100,150,70+n,default_color)
    lcd.fill_rect(100, 105, 90, 90, colour(0, 0, 0))
    for n in range(3):
        lcd.ring(100, 150, 70 - n, colour(128, 128, 128))
    lcd.fill_rect(100, 150, 90, 90, colour(0, 0, 0))
    lcd.vline(100, 200, 30, colour(128, 128, 128))
    lcd.hline(170, 150, 15, colour(128, 128, 128))
    lcd.line(65, 115, 50, 100, colour(128, 128, 128))
    lcd.printstring("0V", 100, 200, 2, 0, 0, default_color)
    lcd.printstring("7.5V", 65, 115, 1, 0, 0, default_color)
    lcd.printstring("15V", 120, 150, 2, 0, 0, default_color)
    lcd.printstring("12.4V", 135, 180, 3, 0, 0, colour(220, 220, 220))
    if voltage:
        # print("Voltage:     ", voltage.split()[1])

        if len(voltage.split()[1]) != 5:
            lcd.fill_rect(25, 120, 40, 40, colour(0, 0, 0))
        else:
            lcd.printstring(f"{voltage.split()[1]}", 25, 120, 3, 0, 0, default_color)
    lcd.show()
    # print("Pressure:    ", pressure)
