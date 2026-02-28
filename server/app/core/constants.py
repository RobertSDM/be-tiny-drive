import os
from server.app.core.schemas import Mode
from shared.constants import MODE

DATABASE_URL = os.getenv("DATABASE_URL")
ORIGINS = os.getenv("ORIGINS").split(";")
JWT_SECRET = os.getenv("JWT_SECRET")

HOST = "0.0.0.0" if MODE == Mode.PROD else "127.0.0.1"
LOG_LEVEL = "info" if MODE == Mode.PROD else "debug"
PORT = int(os.getenv("PORT") or 4500)

## APP CONSTANTS
# limit for file return
LIMIT_PER_PAGE = 12

# limit for search results return
LIMIT_PER_SEARCH = 6

MAX_FILESIZE = 15 * 1024**2
MAX_RECURSIVE_DEPTH = 3
# MAX_FILE_AMOUNT = 15  # rate limit maybe?

## API
non_protected_routes = ["/auth/*"]
