import math
from typing import Callable

from app.database.models.item_model import Item


def pipeline(*funcs: Callable):
    def run(*args, **kwargs):
        result = funcs[0](*args, **kwargs)
        for func in funcs[1:]:
            if result:
                result = func(result)
            else:
                result = func()

        return result

    return run


def normalize_file_size(byte_size: int):
    """
    Transform a size in bytes into a normalized size with its prefix
    """

    prefix = ["b", "Kb", "Mb", "Gb"]

    pos_prefix = 0
    devided_byte = byte_size

    while devided_byte >= 1024 and pos_prefix < len(prefix):
        devided_byte /= 1024
        pos_prefix += 1

    return math.ceil(devided_byte), prefix[pos_prefix]


def make_bucket_path(item: Item):
    """
    Make the bucket path for a storage item file
    """

    return f"user-{item.ownerid}/drive/{item.id}{item.extension}"
