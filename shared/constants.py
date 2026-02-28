import os

MODE = os.getenv("MODE")

SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
SUPA_BUCKETID = os.getenv("SUPA_BUCKET_ID")


SUPPORTED_IMAGE_PREVIEW_TYPES = [
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/tiff",
    "image/jpg",
]

FILE_PROCESSING_QUEUE = "file_processing"
