from machine import Pin, SPI, PWM
import framebuf
import utime
import os
import math

BL = 13  # Pins used for display screen
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

# 7-seg character definations and routines
nums = [
    1,
    1,
    1,
    1,
    1,
    1,
    0,  # 0 # One row per digit
    0,
    1,
    1,
    0,
    0,
    0,
    0,  # 1
    1,
    1,
    0,
    1,
    1,
    0,
    1,  # 2
    1,
    1,
    1,
    1,
    0,
    0,
    1,  # 3
    0,
    1,
    1,
    0,
    0,
    1,
    1,  # 4
    1,
    0,
    1,
    1,
    0,
    1,
    1,  # 5
    1,
    0,
    1,
    1,
    1,
    1,
    1,  # 6
    1,
    1,
    1,
    0,
    0,
    0,
    0,  # 7
    1,
    1,
    1,
    1,
    1,
    1,
    1,  # 8
    1,
    1,
    1,
    0,
    0,
    1,
    1,  # 9
    1,
    1,
    1,
    1,
    1,
    0,
    1,  # a = 10 - HEX characters
    0,
    0,
    1,
    1,
    1,
    1,
    1,  # b = 11
    0,
    0,
    0,
    1,
    1,
    0,
    1,  # c = 12
    0,
    1,
    1,
    1,
    1,
    0,
    1,  # d = 13
    1,
    1,
    0,
    1,
    1,
    1,
    1,  # e = 14
    1,
    0,
    0,
    0,
    1,
    1,
    1,  # f = 15
    1,
    1,
    1,
    1,
    0,
    1,
    1,  # g needed for seg!
    0,
    0,
    0,
    0,
    0,
    0,
    1,  # -
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]  # Blank

# ASCII Character Set
cmap = [
    "00000000000000000000000000000000000",  # Space
    "00100001000010000100001000000000100",  #!
    "01010010100000000000000000000000000",  # "
    "01010010101101100000110110101001010",  ##
    "00100011111000001110000011111000100",  # $
    "11001110010001000100010001001110011",  #%
    "01000101001010001000101011001001101",  # &
    "10000100001000000000000000000000000",  #'
    "00100010001000010000100000100000100",  # (
    "00100000100000100001000010001000100",  # )
    "00000001001010101110101010010000000",  # *
    "00000001000010011111001000010000000",  # +
    "000000000000000000000000000000110000100010000",  # ,
    "00000000000000011111000000000000000",  # -
    "00000000000000000000000001100011000",  # .
    "00001000010001000100010001000010000",  # /
    "01110100011000110101100011000101110",  # 0
    "00100011000010000100001000010001110",  # 1
    "01110100010000101110100001000011111",  # 2
    "01110100010000101110000011000101110",  # 3
    "00010001100101011111000100001000010",  # 4
    "11111100001111000001000011000101110",  # 5
    "01110100001000011110100011000101110",  # 6
    "11111000010001000100010001000010000",  # 7
    "01110100011000101110100011000101110",  # 8
    "01110100011000101111000010000101110",  # 9
    "00000011000110000000011000110000000",  #:
    "01100011000000001100011000010001000",  # ;
    "00010001000100010000010000010000010",  # <
    "00000000001111100000111110000000000",  # =
    "01000001000001000001000100010001000",  # >
    "01100100100001000100001000000000100",  # ?
    "01110100010000101101101011010101110",  # @
    "00100010101000110001111111000110001",  # A
    "11110010010100111110010010100111110",  # B
    "01110100011000010000100001000101110",  # C
    "11110010010100101001010010100111110",  # D
    "11111100001000011100100001000011111",  # E
    "11111100001000011100100001000010000",  # F
    "01110100011000010111100011000101110",  # G
    "10001100011000111111100011000110001",  # H
    "01110001000010000100001000010001110",  # I
    "00111000100001000010000101001001100",  # J
    "10001100101010011000101001001010001",  # K
    "10000100001000010000100001000011111",  # L
    "10001110111010110101100011000110001",  # M
    "10001110011010110011100011000110001",  # N
    "01110100011000110001100011000101110",  # O
    "11110100011000111110100001000010000",  # P
    "01110100011000110001101011001001101",  # Q
    "11110100011000111110101001001010001",  # R
    "01110100011000001110000011000101110",  # S
    "11111001000010000100001000010000100",  # T
    "10001100011000110001100011000101110",  # U
    "10001100011000101010010100010000100",  # V
    "10001100011000110101101011101110001",  # W
    "10001100010101000100010101000110001",  # X
    "10001100010101000100001000010000100",  # Y
    "11111000010001000100010001000011111",  # Z
    "01110010000100001000010000100001110",  # [
    "10000100000100000100000100000100001",  # \
    "00111000010000100001000010000100111",  # ]
    "00100010101000100000000000000000000",  # ^
    "00000000000000000000000000000011111",  # _
    "11000110001000001000000000000000000",  # `
    "00000000000111000001011111000101110",  # a
    "10000100001011011001100011100110110",  # b
    "00000000000011101000010000100000111",  # c
    "00001000010110110011100011001101101",  # d
    "00000000000111010001111111000001110",  # e
    "00110010010100011110010000100001000",  # f
    "000000000001110100011000110001011110000101110",  # g
    "10000100001011011001100011000110001",  # h
    "00100000000110000100001000010001110",  # i
    "0001000000001100001000010000101001001100",  # j
    "10000100001001010100110001010010010",  # k
    "01100001000010000100001000010001110",  # l
    "00000000001101010101101011010110101",  # m
    "00000000001011011001100011000110001",  # n
    "00000000000111010001100011000101110",  # o
    "000000000001110100011000110001111101000010000",  # p
    "000000000001110100011000110001011110000100001",  # q
    "00000000001011011001100001000010000",  # r
    "00000000000111110000011100000111110",  # s
    "00100001000111100100001000010000111",  # t
    "00000000001000110001100011001101101",  # u
    "00000000001000110001100010101000100",  # v
    "00000000001000110001101011010101010",  # w
    "00000000001000101010001000101010001",  # x
    "000000000010001100011000110001011110000101110",  # y
    "00000000001111100010001000100011111",  # z
    "00010001000010001000001000010000010",  # {
    "00100001000010000000001000010000100",  # |
    "01000001000010000010001000010001000",  # }
    "01000101010001000000000000000000000",  # }~
]


def colour(R, G, B):  # Convert 3 byte colours to 2 byte colours, RGB565
    # Get RED value
    rp = int(R * 31 / 255)  # range 0 to 31
    if rp < 0:
        rp = 0
    r = rp * 8
    # Get Green value - more complicated!
    gp = int(G * 63 / 255)  # range 0 - 63
    if gp < 0:
        gp = 0
    g = 0
    if gp & 1:
        g = g + 8192
    if gp & 2:
        g = g + 16384
    if gp & 4:
        g = g + 32768
    if gp & 8:
        g = g + 1
    if gp & 16:
        g = g + 2
    if gp & 32:
        g = g + 4
    # Get BLUE value
    bp = int(B * 31 / 255)  # range 0 - 31
    if bp < 0:
        bp = 0
    b = bp * 256
    colour = r + g + b
    return colour


class LCD_screen(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 1000_000)
        self.spi = SPI(
            1, 100000_000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None
        )
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red = 0x07E0  # Pre-defined colours
        self.green = 0x001F  # Probably easier to use colour(r,g,b) defined below
        self.blue = 0xF800
        self.white = 0xFFFF

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

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

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    def seg(self, xx, yy, n, f, bg, fg):
        # (x, y, number, size-factor, background, foreground)
        c = [bg, fg]
        p = n * 7
        self.fill_rect(xx + 1 * f, yy + 0 * f, 3 * f, 1 * f, c[nums[p]])
        self.fill_rect(xx + 4 * f, yy + 1 * f, 1 * f, 3 * f, c[nums[p + 1]])
        self.fill_rect(xx + 4 * f, yy + 5 * f, 1 * f, 3 * f, c[nums[p + 2]])
        self.fill_rect(xx + 1 * f, yy + 8 * f, 3 * f, 1 * f, c[nums[p + 3]])
        self.fill_rect(xx + 0 * f, yy + 5 * f, 1 * f, 3 * f, c[nums[p + 4]])
        self.fill_rect(xx + 0 * f, yy + 1 * f, 1 * f, 3 * f, c[nums[p + 5]])
        self.fill_rect(xx + 1 * f, yy + 4 * f, 3 * f, 1 * f, c[nums[p + 6]])
        self.show()

    def printchar(self, letter, xpos, ypos, size, charupdate, c):
        origin = xpos
        charval = ord(letter)
        # print(charval)
        index = charval - 32  # start code, 32 or space
        # print(index)
        character = cmap[index]  # this is our char...
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
                        self.pixel(xpos+1,ypos+2,c)
                        self.pixel(xpos+2,ypos+1,c)
                        self.pixel(xpos+2,ypos+2,c)
                        self.pixel(xpos,ypos+2,c)
                        self.pixel(xpos,ypos+2,c)
                        self.pixel(xpos,ypos+1,c)
                        self.pixel(xpos+1,ypos,c)
                        self.pixel(xpos+1,ypos+1,c)
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
