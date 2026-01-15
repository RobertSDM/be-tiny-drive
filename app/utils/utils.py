import io
import math
import re
from PIL import ImageOps
from PIL.ImageFile import ImageFile
from typing import Callable, Literal, Union


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
    if im.size[0] < size[0] or im.size[1] < size[1]:
        return im

    return ImageOps.contain(im, size)


def byte_formatting(byte_size: int):
    """
    Format the size to be more readable
    """

    prefix = ["B", "KB", "MB", "GB"]
    size = byte_size

    for p in prefix:
        if size < 1024:
            return math.ceil(size), p

        size /= 1024


def make_file_bucket_path(
    ownerid: str, fileid: str, type_: Literal["file", "preview"]
) -> str:
    """
    Make the bucket path for the file storage
    """

    match type_:
        case "file":
            return f"user-{ownerid}/drive/{fileid}"
        case "preview":
            return f"user-{ownerid}/preview/{fileid}"


def validate_filename(name: str) -> bool:
    name_regex = r"^[a-zA-Z0-9._\- ]+$"

    if len(name) < 4 or len(name) > 50 or name == "":
        return False

    return re.match(name_regex, name)
