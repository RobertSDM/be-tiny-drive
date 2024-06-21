from fastapi import FastAPI
from routes.FileRest import route as file_route
from routes.FolderRest import folder_router
from fastapi.middleware.cors import CORSMiddleware
from service.logging_config import logger
import dotenv, os, uvicorn

dotenv.load_dotenv()

app = FastAPI(title="Tiny Drive", )

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_route)
app.include_router(folder_router)
    
port = int(os.environ.get("PORT") if os.environ.get("PORT") else 4500)
debug = "info" if os.environ.get("MODE") != "production" else "debug"
host = os.environ.get("HOST") if os.environ.get("HOST") else "0.0.0.0"

if __name__ == "__main__":
    uvicorn.run("main:app", host=host, port=port, reload=True, log_level=debug)
    logger.info("Api started on: " + host + ":" + port)