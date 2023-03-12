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
