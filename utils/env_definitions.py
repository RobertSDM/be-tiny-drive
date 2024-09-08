import os
import dotenv

dotenv.load_dotenv()
Secret_key = os.environ.get("SECRET_KEY")
Database_url = os.environ.get("DATABASE_URL")
Origins = os.environ.get("ORIGINS").split(";")
Port = os.environ.get("PORT") if os.environ.get("PORT") else "4500"
Debug = "info" if os.environ.get("MODE") != "production" else "debug"
Host = os.environ.get("HOST") if os.environ.get("HOST") else "0.0.0.0"

# connection pool
POOL_PRE_PING = os.environ.get("POOL_PRE_PING") 
POOL_SIZE = os.environ.get("POOL_SIZE")
POOL_RECYCLE = os.environ.get("POOL_RECYCLE")
POOL_TIMEOUT = os.environ.get("POOL_TIMEOUT")
