from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from core.schemas import AuthResponse, LoginRequest, RegisterRequest
from database.db_engine import get_session
from service.auth_serv import login_serv, register_serv

auth_router = APIRouter()


@auth_router.post("/login")
def login(user: LoginRequest, db=Depends(get_session)):
    result = login_serv(db, user.email, user.password)

    return JSONResponse(AuthResponse(token=result.token, data=result.user).model_dump())


@auth_router.post("/register")
def register(user: RegisterRequest, db=Depends(get_session)):
    user = register_serv(db, user.username, user.email, user.password)

    return JSONResponse(AuthResponse(data=user).model_dump())
