import os
from typing import Literal

DEFAULT_WORKERS_NUMBER = 2

SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
SUPA_BUCKETID = os.getenv("SUPA_BUCKET_ID")
PROCESSING_QUEUE_URL = os.getenv("PROCESSING_QUEUE_URL")


SUPPORTED_IMAGE_PREVIEW_TYPES = [
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/tiff",
    "image/jpg",
]

FILE_PROCESSING_QUEUE = "file_processing"

PREVIEW_SIZES = Literal["large", "medium", "small"]
BUCKET_PATH_TYPES = Literal["file", "preview+large", "preview+small", "preview+medium"]
