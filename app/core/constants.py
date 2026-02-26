import os
from app.core.schemas import Mode
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE")
DATABASE_URL = os.getenv("DATABASE_URL")
ORIGINS = os.getenv("ORIGINS").split(";")

JWT_SECRET = os.getenv("JWT_SECRET")

SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
SUPA_BUCKETID = os.getenv("SUPA_BUCKET_ID")

HOST = "0.0.0.0" if MODE == Mode.PROD else "127.0.0.1"

LOG_LEVEL = "info" if MODE == Mode.PROD else "debug"

PORT = int(os.getenv("PORT") or 4500)


## App Constants

FILE_PROCESSING_QUEUE = "file_processing"

# limit for file return
LIMIT_PER_PAGE = 12

# limit for search results return
LIMIT_PER_SEARCH = 6

MAX_FILESIZE = 15 * 1024**2
MAX_RECURSIVE_DEPTH = 3
# MAX_FILE_AMOUNT = 15  # rate limit maybe?

SUPPORTED_IMAGE_PREVIEW_TYPES = [
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/tiff",
    "image/jpg",
]


## API

non_protected_routes = ["/auth/*", "/send"]
