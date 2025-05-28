import math
from typing import Callable

import zstandard

from app.database.models.item_model import Item


def reducer(*funcs: Callable):
    def run(*args, **kwargs):
        result = funcs[0](*args, **kwargs)
        for func in funcs[1:]:
            if result:
                result = func(result)
            else:
                result = func()

        return result

    return run

def compress_file(file: bytes) -> bytes:
    cctx = zstandard.ZstdCompressor()
    return cctx.compress(file)

def decompress_file(file: bytes) -> bytes:
    dctx = zstandard.ZstdDecompressor()
    return dctx.decompress(file)

def normalize_file_size(byte_size: int):
    """
    Transform a size in bytes into a normalized size with its prefix
    """

    prefix = ["B", "KB", "MB", "GB"]
    size = byte_size

    for p in prefix:
        if size < 1024:
            return math.ceil(size), p

        size /= 1024


def make_bucket_path(item: Item):
    """
    Make the bucket path for a storage item file
    """

    return f"user-{item.ownerid}/drive/{item.id}{item.extension}"
