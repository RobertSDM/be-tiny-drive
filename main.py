import json
from typing import final
from fastapi import Depends, FastAPI, Request, Response
from sqlalchemy.orm import Session
from database.init_database import get_session
from routes.FileRest import route as file_route
from routes.FolderRest import folder_router
from routes.AuthRest import auth_router
from fastapi.middleware.cors import CORSMiddleware
from service.logging_config import logger
import dotenv, os, uvicorn

from service.user_auth_serv import validate_token_serv

dotenv.load_dotenv()


app = FastAPI(
    title="Tiny Drive",
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ORIGINS").split(";"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    all_access_routes = ["/auth/register", "/auth/login"]
    path = request.url.path
    print(request.method)

    if path not in all_access_routes and request.method != "OPTIONS":
        token = request.cookies.get("c_token")
        print(request.cookies)

        if not token:
            return Response(
                status_code=422,
                content=json.dumps({"msg": "token no exist", "data": None}),
            )

        db: Session = next(get_session())

        try:
            res = validate_token_serv(db, token)
        finally:
            db.close()

        if not isinstance(res, bool):
            return Response(
                status_code=res["status"], content=json.dumps(res["content"])
            )

    return await call_next(request)


app.include_router(file_route)
app.include_router(folder_router)
app.include_router(auth_router)

port = int(os.environ.get("PORT") if os.environ.get("PORT") else 4500)
debug = "info" if os.environ.get("MODE") != "production" else "debug"
host = os.environ.get("HOST") if os.environ.get("HOST") else "0.0.0.0"

if __name__ == "__main__":
    uvicorn.run("main:app", host=host, port=port, reload=True, log_level=debug)
    logger.info("Api started on: " + host + ":" + port)
