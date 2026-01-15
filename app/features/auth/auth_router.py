from re import A
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field
from app.core.authentication_client_singleton import AuthClientSingleton
from app.core.schemas import AccountReturnable
from app.lib.sqlalchemy import client
from sqlalchemy.orm import Session

from app.features.auth.services.AuthenticationService import AuthenticationService

auth_router = APIRouter()


class RegisterBody(BaseModel):
    username: Annotated[str, Field(min_length=4, max_length=50)]
    email: Annotated[
        str, Field(min_length=6, max_length=50, pattern=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$")
    ]
    password: Annotated[str, Field(min_length=8, max_length=50)]


@auth_router.post("/register")
def register(
    body: RegisterBody,
    db: Session = Depends(client.get_session),
    auth_client=Depends(AuthClientSingleton.get_instance),
):
    auth_service = AuthenticationService(auth_client)
    account = auth_service.register_serv(db, body.username, body.email, body.password)

    return ORJSONResponse(AccountReturnable(data=account).model_dump())
