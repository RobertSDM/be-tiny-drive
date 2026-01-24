from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field
from app.core.authentication_client_singleton import (
    get_auth_service,
)
from app.core.schemas import AccountDTO
from app.interfaces.authentication_interface import AuthenticationInterface
from app.lib.sqlalchemy import client
from sqlalchemy.orm import Session

from app.features.auth.services.AuthenticationService import AuthenticationService

auth_router = APIRouter()


class LoginBody(BaseModel):
    email: str = Field(min_length=6, max_length=50)
    password: str = Field(min_length=8, max_length=50)


@auth_router.post("/login")
def login_route(
    body: LoginBody,
    auth_client: AuthenticationInterface = Depends(get_auth_service),
):
    user_data = auth_client.login(body.email, body.password)

    return ORJSONResponse(user_data.model_dump())


class RegisterBody(BaseModel):
    username: str = Field(min_length=4, max_length=50)
    email: str = Field(min_length=6, max_length=50)
    password: str = Field(min_length=8, max_length=50)


@auth_router.post("/register")
def register_route(
    body: RegisterBody,
    db: Session = Depends(client.get_session),
):
    auth_service = AuthenticationService(get_auth_service())
    account = auth_service.register(db, body.username, body.email, body.password)

    return ORJSONResponse(account)
