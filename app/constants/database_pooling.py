import os

# connection pool
POOL_PRE_PING = os.getenv("POOL_PRE_PING")
POOL_SIZE = os.getenv("POOL_SIZE")
POOL_RECYCLE = os.getenv("POOL_RECYCLE")
POOL_TIMEOUT = os.getenv("POOL_TIMEOUT")
