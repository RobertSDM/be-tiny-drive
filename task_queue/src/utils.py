import io

from PIL import ImageOps
from PIL.ImageFile import ImageFile

from task_queue.src.constants import BUCKET_PATH_TYPES


def make_file_bucket_path(
    ownerid: str,
    fileid: str,
    type_: BUCKET_PATH_TYPES,
) -> str:
    """
    Make the bucket path for the file storage
    """

    match type_:
        case "file":
            return f"user-{ownerid}/drive/{fileid}"
        case "preview+large":
            return f"user-{ownerid}/preview/large/{fileid}"
        case "preview+medium":
            return f"user-{ownerid}/preview/medium/{fileid}"
        case "preview+small":
            return f"user-{ownerid}/preview/small/{fileid}"


def image_to_jpg(im: ImageFile, quality: int = 70) -> io.BytesIO:
    buffer = io.BytesIO()

    if im.mode != "RGB":
        im = im.convert("RGB")

    if im.mode in ["JPEG", "JPG"]:
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
