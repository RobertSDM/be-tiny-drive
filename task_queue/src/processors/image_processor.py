import io

from PIL import Image
from PIL.ImageFile import ImageFile
from task_queue.src.utils import resize_image

from task_queue.src.constants import SUPPORTED_IMAGE_PREVIEW_TYPES


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


def image_processing(tempfile_: str, content_type: str) -> None:
    if content_type not in SUPPORTED_IMAGE_PREVIEW_TYPES:
        return None

    image = Image.open(tempfile_)
    image = resize_image(image)
    image = image_to_jpg(image)

    return image
