from constant import EOM_default

# utils functions
def bytes_to_int(bs):
    """converts a big-endian byte array into a single integer"""
    v = 0
    p = 0
    for b in reversed(bs):
        v += b * (2**p)
        p += 8
    return v


def decode_temperature(message):
    """Temperature is in the -40:215 celsius range as int."""

    return bytes_to_int(message[2:]) - 40


def decode_pressure(message):
    """Pressure is in the 0:255 kPa range as int."""

    return int(message[2])


def decode_percent(message):
    """Percent is in the 0:100 range as float."""

    return int(message[2]) * 100.0 / 255.0


def decode_rpm(message):
    """RPM is in the 0:16384 revs/min range as int."""

    return bytes_to_int(message[2:]) / 4


def decode_speed(message):
    """Speed is in the 0:255 km/h range as int."""

    return int(message[2])


def decode_message(message):
    """Function for decoding messages from elm327"""

    decoded_message = ""
    message_list = [char for char in message]

    while message_list[0] == 13:
        message_list.pop(0)

    for char in message_list:
        decoded_message += chr(char)

    print("decoded:   ", decoded_message)
    return decoded_message
