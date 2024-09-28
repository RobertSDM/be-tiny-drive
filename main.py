import json
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Response
from api.routes.file_rest import file_router
from api.routes.folder_rest import folder_router
from api.routes.auth_rest import auth_router
from api.routes.content_rest import content_router
from fastapi.middleware.cors import CORSMiddleware
from database.init_database import get_session
from service.logging_config import logger
from service.user_auth_serv import validate_token_serv
from project.variables.env_definitions import Debug, Host, Origins, Port
import uvicorn

app = FastAPI(title="Tiny Drive", description="Backend api for tiny-drive project")

## Middlewares
# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=Origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


## APIRoutes
app.include_router(file_router, prefix="/file")
app.include_router(folder_router, prefix="/folder")
app.include_router(auth_router, prefix="/auth")
app.include_router(content_router, prefix="/content")


def get_app() -> FastAPI:
    return app


if __name__ == "__main__":
    logger.info("App stated on -> : " + Host + ":" + Port)
    uvicorn.run("main:app", host=Host, port=int(Port), reload=True, log_level=Debug)
