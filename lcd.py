from machine import Pin, SPI, PWM
import framebuf
import math
from fonts import CMAP, NUMS
from lcd_utils import colour


class LCD(framebuf.FrameBuffer):
    def __init__(
        self,
        pin_BL,
        pin_DC,
        pin_RST,
        pin_MOSI,
        pin_SCK,
        pin_CS,
        width,
        height,
        spi_id,
        spi_baudrate,
        spi_polarity,
        spi_phase,
        default_red,
        default_green,
        default_blue,
        default_white,
    ):
        self.width = width
        self.height = height

        self.cs = Pin(pin_CS, Pin.OUT)
        self.rst = Pin(pin_RST, Pin.OUT)

        self.cs.value(spi_id)
        self.spi = SPI(spi_id)
        self.spi = SPI(spi_id, spi_baudrate)
        self.spi = SPI(
            spi_id,
            spi_baudrate,
            polarity=spi_polarity,
            phase=spi_phase,
            sck=Pin(pin_SCK),
            mosi=Pin(pin_MOSI),
            miso=None,
        )
        self.dc = Pin(pin_DC, Pin.OUT)
        self.dc.value(spi_id)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red = default_red  # Pre-defined colours
        self.green = default_green  # Probably easier to use colour(r,g,b) defined below
        self.blue = default_blue
        self.white = default_white

    def write_cmd(self, cmd):
        self.cs.value(1)
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, buf):
        self.cs.value(1)
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(bytearray([buf]))
        self.cs.value(1)

    def init_display(self):
        """Initialize display"""
        self.rst.value(1)
        self.rst.value(0)
        self.rst.value(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        self.write_cmd(0x2C)

        self.cs.value(1)
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(self.buffer)
        self.cs.value(1)

    def seg(self, xx, yy, n, f, bg, fg):
        # (x, y, number, size-factor, background, foreground)
        c = [bg, fg]
        p = n * 7
        self.fill_rect(xx + 1 * f, yy + 0 * f, 3 * f, 1 * f, c[NUMS[p]])
        self.fill_rect(xx + 4 * f, yy + 1 * f, 1 * f, 3 * f, c[NUMS[p + 1]])
        self.fill_rect(xx + 4 * f, yy + 5 * f, 1 * f, 3 * f, c[NUMS[p + 2]])
        self.fill_rect(xx + 1 * f, yy + 8 * f, 3 * f, 1 * f, c[NUMS[p + 3]])
        self.fill_rect(xx + 0 * f, yy + 5 * f, 1 * f, 3 * f, c[NUMS[p + 4]])
        self.fill_rect(xx + 0 * f, yy + 1 * f, 1 * f, 3 * f, c[NUMS[p + 5]])
        self.fill_rect(xx + 1 * f, yy + 4 * f, 3 * f, 1 * f, c[NUMS[p + 6]])
        self.show()

    def printchar(self, letter, xpos, ypos, size, charupdate, c):
        origin = xpos
        charval = ord(letter)
        # print(charval)
        index = charval - 32  # start code, 32 or space
        # print(index)
        character = CMAP[index]  # this is our char...
        rows = [character[i : i + 5] for i in range(0, len(character), 5)]
        # print(rows)
        for row in rows:
            # print(row)
            for bit in row:
                # print(bit)
                if bit == "1":
                    self.pixel(xpos, ypos, c)
                    if size == 2:
                        self.pixel(xpos, ypos + 1, c)
                        self.pixel(xpos + 1, ypos, c)
                        self.pixel(xpos + 1, ypos + 1, c)
                    if size == 3:
                        self.pixel(xpos + 1, ypos + 2, c)
                        self.pixel(xpos + 2, ypos + 1, c)
                        self.pixel(xpos + 2, ypos + 2, c)
                        self.pixel(xpos, ypos + 2, c)
                        self.pixel(xpos, ypos + 2, c)
                        self.pixel(xpos, ypos + 1, c)
                        self.pixel(xpos + 1, ypos, c)
                        self.pixel(xpos + 1, ypos + 1, c)
                xpos += size
            xpos = origin
            ypos += size
        if charupdate == True:
            self.show()

    def delchar(self, xpos, ypos, size, delupdate):
        if size == 1:
            charwidth = 5
            charheight = 9
        elif size == 2:
            charwidth = 10
            charheight = 18
        elif size == 3:
            charwidth = 15
            charheight = 27
        else:
            charwidth = 15
            charheight = 27
        c = colour(0, 0, 0)  # Colour of background
        self.fill_rect(xpos, ypos, charwidth, charheight, c)  # xywh
        if delupdate == True:
            self.show()

    def printstring(self, string, xpos, ypos, size, charupdate, strupdate, c):
        if size == 1:
            spacing = 8
        elif size == 2:
            spacing = 14
        elif size == 3:
            spacing = 18
        else:
            spacing = 18
        for i in string:
            self.printchar(i, xpos, ypos, size, charupdate, c)
            xpos += spacing
        if strupdate == True:
            self.show()

    def ring(self, cx, cy, r, cc):  # Draws a circle - with centre (x,y), radius, colour
        for angle in range(91):  # 0 to 90 degrees in 2s
            y3 = int(r * math.sin(math.radians(angle)))
            x3 = int(r * math.cos(math.radians(angle)))
            self.pixel(cx - x3, cy + y3, cc)  # 4 quadrants
            self.pixel(cx - x3, cy - y3, cc)
            self.pixel(cx + x3, cy + y3, cc)
            self.pixel(cx + x3, cy - y3, cc)
