import json
from fastapi import APIRouter, Depends, Response
from schemas.schemas import UserParamLoginSchema, UserParamRegisterSchema
from database.db_engine import get_session
from service.user_auth_serv import log_user_serv, register_serv

auth_router = APIRouter()


@auth_router.post("/login")
def __login(user: UserParamLoginSchema, db=Depends(get_session)):
    res = log_user_serv(db, user.email, user.password)

    response = Response(status_code=res["status"], content=json.dumps(res["content"]))

    return response


@auth_router.post("/register")
def __register(user: UserParamRegisterSchema, db=Depends(get_session)):
    res = register_serv(db, user)

    return Response(status_code=res["status"], content=json.dumps(res["content"]))
