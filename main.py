from fastapi import FastAPI
from api.routes.item_route import item_router
from api.routes.auth_route import auth_router
from fastapi.middleware.cors import CORSMiddleware
from service.logging_config import logger
from constants.env_definitions import debug, host, origins, port
import uvicorn

app = FastAPI(title="Tiny Drive", description="Backend API for tiny-drive project")

## Middlewares
# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


## APIRoutes
app.include_router(item_router, prefix="/item")
# app.include_router(file_router, prefix="/file")
# app.include_router(folder_router, prefix="/folder")
app.include_router(auth_router, prefix="/auth")
# app.include_router(content_router, prefix="/content")


def get_app() -> FastAPI:
    return app


if __name__ == "__main__":
    logger.info("App stated on -> : " + host + ":" + port)
    uvicorn.run("main:app", host=host, port=int(port), reload=True, log_level=debug)
