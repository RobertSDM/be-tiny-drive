import os
from app.core.schemas import Mode

default_db_url = "postgresql://postgres:password@localhost:5432/postgres"

MODE = os.getenv("MODE")

DATABASE_URL = os.getenv("DATABASE_URL") if MODE == Mode.PROD.value else default_db_url

ORIGINS = os.getenv("ORIGINS").split(";")
PORT = int(os.getenv("PORT") or 4500)

JWT_SECRET = os.getenv("JWT_SECRET")

SUPA_URL = os.getenv("SUPA_URL")
SUPA_KEY = os.getenv("SUPA_KEY")
SUPA_BUCKETID = (
    os.getenv("SUPA_BUCKET_ID") if MODE == Mode.PROD.value else "drive-files-dev"
)

##

LOG_LEVEL = "info" if MODE == Mode.PROD.value else "debug"

HOST = "0.0.0.0"

# limit for file return
LIMIT_PER_PAGE = 20

# limit for search results return
LIMIT_PER_SEARCH = 6

MAX_RECURSIVE_DEPTH = 3
MAX_FILE_AMOUNT = 15  # rate limit maybe?
