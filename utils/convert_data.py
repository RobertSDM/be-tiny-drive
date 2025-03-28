import base64
import io
import math


def get_sufix_to_bytes(byte_size: int):
    prefix = ["b", "Kb", "Mb", "Gb"]

    pos_prefix = 0
    devided_byte = byte_size

    while devided_byte >= 1024 and pos_prefix < len(prefix) - 1:
        devided_byte /= 1024
        pos_prefix += 1

    return math.ceil(devided_byte), prefix[pos_prefix]


def get_base64_to_bytes_data(byte_data: base64) -> io.BytesIO:
    base64_data = base64.b64decode(byte_data)
    return io.BytesIO(base64_data)
