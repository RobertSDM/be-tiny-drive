from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AccountDoesNotExists,
    NoAuthorizationHeader,
    IndentityMismatch,
)
from app.core.select_dependency import AuthClientSingleton
from app.database.client.sqlalchemy_client import db_client
from app.database.repositories.account_repo import account_by_id
from app.decorators.timer import timer
from app.interfaces.authentication_interface import AuthenticationInterface
from app.utils.query import exec_exists, exec_first


async def auth_middleware(
    req: Request,
    auth_client: AuthenticationInterface = Depends(
        AuthClientSingleton.get_auth_client_instance
    ),
    db: Session = Depends(db_client.get_session),
):
    authorization = req.headers.get("Authorization")
    if not authorization:
        raise NoAuthorizationHeader()

    token = authorization.replace("Bearer ", "")
    resp = auth_client.verifyToken(token)

    exists = exec_first(account_by_id(db, resp["sub"]))

    if not exists:
        raise AccountDoesNotExists()

    ownerid = req.path_params.get("ownerid", None)
    if ownerid and ownerid != resp["sub"]:
        raise IndentityMismatch()
