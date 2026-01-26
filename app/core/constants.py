import os
from app.core.schemas import Mode
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE")
DATABASE_URL = os.getenv("DATABASE_URL")
ORIGINS = os.getenv("ORIGINS").split(";")
PORT = int(os.getenv("PORT") or 4500)

JWT_SECRET = os.getenv("JWT_SECRET")

SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
SUPA_BUCKETID = os.getenv("SUPA_BUCKET_ID")

## 

LOG_LEVEL = "info" if MODE == Mode.PROD.value else "debug"

HOST = "0.0.0.0" if MODE == Mode.PROD.value else "127.0.0.1"

## App Constants

# limit for file return
LIMIT_PER_PAGE = 12

# limit for search results return
LIMIT_PER_SEARCH = 6

MAX_FILESIZE = 15 * 1024**2
MAX_RECURSIVE_DEPTH = 3
# MAX_FILE_AMOUNT = 15  # rate limit maybe?

## API

non_protected_routes = ["/auth/*", "^/$"]
