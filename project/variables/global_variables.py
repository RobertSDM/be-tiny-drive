import os, dotenv

dotenv.load_dotenv()
# connection pool
POOL_PRE_PING = os.environ.get("POOL_PRE_PING")
POOL_SIZE = os.environ.get("POOL_SIZE")
POOL_RECYCLE = os.environ.get("POOL_RECYCLE")
POOL_TIMEOUT = os.environ.get("POOL_TIMEOUT")

# pagination
TAKE_PER_PAGE = 8
