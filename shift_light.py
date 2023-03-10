import machine, neopixel
from time import sleep

neo_pixel = neopixel.NeoPixel(machine.Pin(4), 8)

for n in range(8):
    neo_pixel[n] = (0, 0, 0)


def segment1(neo_pixel):
    neo_pixel[0] = (50, 0, 0)
    neo_pixel[1] = (50, 0, 0)


def segment2(neo_pixel):
    neo_pixel[2] = (50, 0, 0)
    neo_pixel[3] = (50, 0, 0)


def segment3(neo_pixel):
    neo_pixel[4] = (50, 0, 0)
    neo_pixel[5] = (50, 0, 0)


def segment4(neo_pixel):
    neo_pixel[6] = (50, 0, 0)
    neo_pixel[7] = (50, 0, 0)


def segment_limit_on(neo_pixel):
    for n in range(8):
        neo_pixel[n] = (0, 0, 125)


def segment_limit_off(neo_pixel):
    for n in range(8):
        neo_pixel[n] = (0, 0, 0)


limiter = False
while True:

    for rpm in range(0, 6500, 100):

        sleep(0.05)
        print("RPM: ", rpm)
        for n in range(8):
            neo_pixel[n] = (0, 0, 0)

        if rpm < 4000:
            segment_limit_off(neo_pixel)
            neo_pixel.write()
        if 4000 < rpm <= 4500:
            segment1(neo_pixel)
            neo_pixel.write()
        if 4500 < rpm <= 5000:
            segment1(neo_pixel)
            segment2(neo_pixel)
            neo_pixel.write()
        if 5000 < rpm <= 5500:
            segment1(neo_pixel)
            segment2(neo_pixel)
            segment3(neo_pixel)
            neo_pixel.write()
        if 5500 < rpm <= 6000:
            segment1(neo_pixel)
            segment2(neo_pixel)
            segment3(neo_pixel)
            segment4(neo_pixel)
            neo_pixel.write()
        if rpm > 6000:
            segment_limit_on(neo_pixel)
            neo_pixel.write()
            segment_limit_off(neo_pixel)
            neo_pixel.write()

    for rpm in range(6500, 0, -100):

        sleep(0.05)
        print("RPM: ", rpm)
        for n in range(8):
            neo_pixel[n] = (0, 0, 0)

        if rpm < 4000:
            segment_limit_off(neo_pixel)
            neo_pixel.write()
        if 4000 < rpm <= 4500:
            segment1(neo_pixel)
            neo_pixel.write()
        if 4500 < rpm <= 5000:
            segment1(neo_pixel)
            segment2(neo_pixel)
            neo_pixel.write()
        if 5000 < rpm <= 5500:
            segment1(neo_pixel)
            segment2(neo_pixel)
            segment3(neo_pixel)
            neo_pixel.write()
        if 5500 < rpm <= 6000:
            segment1(neo_pixel)
            segment2(neo_pixel)
            segment3(neo_pixel)
            segment4(neo_pixel)
            neo_pixel.write()
        if rpm > 6000:
            segment_limit_on(neo_pixel)
            neo_pixel.write()
            segment_limit_off(neo_pixel)
            neo_pixel.write()
