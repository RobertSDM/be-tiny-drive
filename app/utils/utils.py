import io
import math
from PIL import Image, ImageOps
from PIL.ImageFile import ImageFile
from typing import Callable

import zstandard

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


def compress_file(file: bytes) -> bytes:
    cctx = zstandard.ZstdCompressor()
    return cctx.compress(file)


def decompress(file: bytes) -> bytes:
    dctx = zstandard.ZstdDecompressor()
    return dctx.decompress(file)


def image_to_jpg(im: ImageFile, quality: int = 70) -> io.BytesIO:
    buffer = io.BytesIO()

    if im.mode != "RGB":
        im = im.convert("RGB")
    elif im.mode == "JPEG" or im.mode == "JPG":
        im.save(buffer)
        buffer.seek(0)
        return buffer

    im.save(buffer, "JPEG", optimize=True, quality=quality)

    buffer.seek(0)
    return buffer


def resize_image(im: ImageFile, size: tuple[int, int] = (1920, 1080)) -> ImageFile:
    return ImageOps.contain(im, size)


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


def make_bucket_file_path(item: Item) -> str:
    """
    Make the bucket path for a storage item file
    """

    return f"user-{item.ownerid}/drive/{item.id}"


def make_bucket_file_preview_path(item: Item) -> str:
    return f"user-{item.ownerid}/preview/{item.id}"
