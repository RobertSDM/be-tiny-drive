import io
from typing import Literal

from PIL import ImageOps
from PIL.ImageFile import ImageFile


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


def resize_image(im: ImageFile, size: tuple[int, int] = (1920, 1080)) -> ImageFile:
    if im.size[0] < size[0] or im.size[1] < size[1]:
        return im

    return ImageOps.contain(im, size)
