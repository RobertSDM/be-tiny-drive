import json
from service.logging_config import logger
from fastapi import APIRouter, Depends, Response
from database.schemas import UserParamLoginSchema, UserParamRegisterSchema
from database.init_database import get_session
from service.user_auth_serv import log_user_serv, pass_hashing_serv

auth_router = APIRouter()


@auth_router.post("/login")
def __login(user: UserParamLoginSchema, db=Depends(get_session)):
    res = log_user_serv(db, user.email, user.password)

    print(json.dumps(res, indent=4))

    response = Response(
        status_code=res["status"], content=json.dumps(res["content"])
    )

    return response


@auth_router.post("/register")
def __register(user: UserParamRegisterSchema, db=Depends(get_session)):
    res = pass_hashing_serv(db, user)

    return Response(status_code=res["status"], content=json.dumps(res["content"]))
