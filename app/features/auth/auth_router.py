from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.exceptions import NoAuthorizationHeader
from app.lib.sqlalchemy import client
from app.features.auth.services.AuthenticationService import AuthenticationService
from app.lib.supabase.authentication import supa_authentication

auth_router = APIRouter()


class LoginBody(BaseModel):
    email: str = Field(min_length=6, max_length=50)
    password: str = Field(min_length=8, max_length=50)


@auth_router.post("/login")
def login_route(
    body: LoginBody,
    response: ORJSONResponse,
):
    user_data = AuthenticationService(supa_authentication).login(
        body.email, body.password
    )

    return user_data


@auth_router.post("/logout")
def logout_route(request: Request):
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise NoAuthorizationHeader()

    jwt = authorization.replace("Bearer ", "")

    AuthenticationService(supa_authentication).logout(jwt)

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
    auth_service = AuthenticationService(supa_authentication)
    account = auth_service.register(db, body.username, body.email, body.password)

    return ORJSONResponse(account)
