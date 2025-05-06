import dotenv, os

dotenv.load_dotenv()

# Global enviroment variables
mode = os.environ.get("MODE")
secret_key = os.environ.get("SECRET_KEY")
database_url = (
    os.environ.get("DATABASE_URL") if mode == "prod" else "sqlite:///database.db"
)
origins = os.environ.get("ORIGINS").split(";")
port = os.environ.get("PORT") if os.environ.get("PORT") else "4500"
debug = "info" if mode == "prod" else "debug"
host = os.environ.get("HOST") if os.environ.get("HOST") else "0.0.0.0"
clients_URL = os.environ.get("CLIENTS_URL")
