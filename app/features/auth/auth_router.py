from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import ORJSONResponse
import gotrue
import gotrue.errors
from pydantic import BaseModel, Field
from app.core.authentication_client_singleton import (
    get_auth_service,
)
from app.core.exceptions import NoAuthorizationHeader
from app.core.schemas import AccountDTO, ErrorResponse
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
    response: ORJSONResponse,
    auth_client: AuthenticationInterface = Depends(get_auth_service),
):
    try:
        user_data = auth_client.login(body.email, body.password)
    except gotrue.errors.AuthApiError:
        response.status_code = 422

        return ErrorResponse(message="Email or password are wrong")

    return user_data


@auth_router.post("/logout")
def logout_route(request: Request):
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise NoAuthorizationHeader()

    jwt = authorization.replace("Bearer ", "")

    isLoggedOut = get_auth_service().logout(jwt)

    if not isLoggedOut:
        return Response(status_code=404)

    return Response(status_code=200)


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
