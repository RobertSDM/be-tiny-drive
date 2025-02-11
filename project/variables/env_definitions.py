import dotenv, os

dotenv.load_dotenv()

print(os.environ.get("CLIENTS_URL"))

# Global enviroment variables
Secret_key = os.environ.get("SECRET_KEY")
Database_url = os.environ.get("DATABASE_URL")
Origins = os.environ.get("ORIGINS").split(";")
Port = os.environ.get("PORT") if os.environ.get("PORT") else "4500"
Debug = "info" if os.environ.get("MODE") != "production" else "debug"
Host = os.environ.get("HOST") if os.environ.get("HOST") else "0.0.0.0"
Clients_URL = os.environ.get("CLIENTS_URL")
