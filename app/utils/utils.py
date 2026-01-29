import io
import math
import re
from PIL import ImageOps
from PIL.ImageFile import ImageFile
from typing import Literal


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
    ownerid: str,
    fileid: str,
    type_: Literal["file", "preview", "trash+preview", "trash+file"],
) -> str:
    """
    Make the bucket path for the file storage
    """

    match type_:
        case "file":
            return f"user-{ownerid}/drive/{fileid}"
        case "preview":
            return f"user-{ownerid}/preview/{fileid}"
        case "trash+file":
            return f"user-{ownerid}/trash/drive/{fileid}"
        case "trash+preview":
            return f"user-{ownerid}/trash/preview/{fileid}"


def validate_filename(name: str) -> bool:

    name_regex = r"^[\^\<\>\*\?\\\|\"\'\:]$"
    # 260 is the maximum filename length in windows.
    # It's the largest of other OS
    if name == "" or len(name) > 260:
        return False

    return re.match(name_regex, name) is None
