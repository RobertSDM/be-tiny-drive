import io
from typing import List, Tuple

from PIL import Image
from task_queue.src.utils import image_to_jpg, resize_image

from task_queue.src.constants import PREVIEW_SIZES, SUPPORTED_IMAGE_PREVIEW_TYPES


def preview_processing(
    image: Image, content_type: str
) -> List[Tuple[PREVIEW_SIZES, io.BytesIO]]:
    if content_type not in SUPPORTED_IMAGE_PREVIEW_TYPES:
        return None

    large = resize_image(image)
    large = image_to_jpg(large)

    medium = resize_image(image, (1280, 720))
    medium = image_to_jpg(medium, 60)

    small = resize_image(image, (640, 360))
    small = image_to_jpg(small, 60)

    return [("large", large), ("medium", medium), ("small", small)]
