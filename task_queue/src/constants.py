import os

DEFAULT_WORKERS_NUMBER = 2

MODE = os.getenv("MODE")

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
