import os
from app.enums.enums import Mode


mode = os.getenv("MODE")
database_url = os.getenv("DATABASE_URL")
origins = os.getenv("ORIGINS")
port = os.getenv("PORT")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
drive_bucketid = os.getenv("STORAGE_BUCKET_ID")

database_url = (
    database_url
    if mode == Mode.PROD.value
    else "postgresql://postgres:password@localhost:5432/postgres"
)
origins = origins.split(";")
port = int(port if port else 4500)
debug = "info" if mode == Mode.PROD.value else "debug"
host = "0.0.0.0"
drive_bucketid = drive_bucketid if mode == Mode.PROD.value else "drive-files-dev"
