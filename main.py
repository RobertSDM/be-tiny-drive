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
from utils.env_definitions import Debug, Host, Origins, Port
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


@app.middleware("http")
async def verify_auth_header(request: Request, call_next):
    all_access_routes = ("/auth/register", "/auth/login")
    path = request.url.path

    if not path.startswith(all_access_routes) and request.method != "OPTIONS":
        jwt_token = request.headers.get("Authorization")

        if not jwt_token:
            return Response(
                status_code=422,
                content=json.dumps(
                    {"msg": "Authorization header not informed", "data": None}
                ),
            )

        db: Session = next(get_session())

        try:
            res = validate_token_serv(db, jwt_token)
        finally:
            db.close()

        if not isinstance(res, bool):
            return Response(
                status_code=res["status"], content=json.dumps(res["content"])
            )

    return await call_next(request)


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
