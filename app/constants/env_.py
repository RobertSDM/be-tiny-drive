import os

from app.enums.enums import Mode


# Environment variables
mode = os.getenv("MODE")
database_url = os.getenv("DATABASE_URL")
origins = os.getenv("ORIGINS")
port = os.getenv("PORT")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
drive_bucketid = os.getenv("STORAGE_BUCKET_ID")

database_url = database_url if mode == Mode.PROD else "sqlite:///database.db"
origins = origins.split(";")
port = int(port if port else 4500)
debug = "info" if mode == Mode.PROD else "debug"
host = "0.0.0.0"
