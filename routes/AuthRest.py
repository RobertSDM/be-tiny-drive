import json
from fastapi import APIRouter, Depends, Response
from database.models.UserModel import User
from database.schemas.schemas import UserParamLoginSchema, UserParamRegisterSchema, UserSchema
from database.init_database import get_session
from service.user_auth_serv import log_user_serv, pass_hashing_serv

auth_router = APIRouter()


@auth_router.post("/auth/login")
def login(user: UserParamLoginSchema, db=Depends(get_session)):
    res = log_user_serv(db, user.email, user.password)

    return Response(status_code=res["status"], content=json.dumps(res["content"]))


@auth_router.post("/auth/register")
def register(user: UserParamRegisterSchema, db=Depends(get_session)):
    res = pass_hashing_serv(db, user)
    
    return Response(status_code=res["status"], content=json.dumps(res["content"]))
