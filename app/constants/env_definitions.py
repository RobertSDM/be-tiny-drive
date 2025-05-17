import os

from app.enums.enums import Mode


# Environment variables
mode = os.getenv("MODE")
secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")
origins = os.getenv("ORIGINS")
port = os.getenv("PORT")
host = os.getenv("HOST")
clients_URL = os.getenv("CLIENTS_URL")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

database_url = database_url if mode == Mode.PROD else "sqlite:///database.db"
origins = origins.split(";")
port = int(port if port else 4500)
debug = "info" if mode == Mode.PROD else "debug"
host = host if host else "127.0.0.1"
