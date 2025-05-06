import json
from fastapi import APIRouter, Depends, Response
from schemas.schemas import UserParamLoginSchema, UserParamRegisterSchema
from database.db_engine import get_session
from service.auth_serv import login_serv, register_serv

auth_router = APIRouter()


@auth_router.post("/login")
def login(user: UserParamLoginSchema, db=Depends(get_session)):
    res = login_serv(db, user.email, user.password)

    response = Response(status_code=res["status"], content=json.dumps(res["content"]))

    return response


@auth_router.post("/register")
def register(user: UserParamRegisterSchema, db=Depends(get_session)):
    res = register_serv(db, user.username, user.email, user.password)

    if not res:
        return Response(status_code=409)

    return Response(status_code=200, content=res.__dict__)
