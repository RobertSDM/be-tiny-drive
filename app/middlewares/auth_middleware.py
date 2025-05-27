from typing import Annotated
from fastapi import Depends, Request

from app.core.exceptions import (
    AccountDoesNotExists,
    NoAuthorizationHeader,
    IndentityMismatch,
)
from app.core.select_dependency import get_auth_client_instance
from app.database.client.sqlalchemy_client import db_client
from app.database.repositories.account_repo import account_by_id
from app.interfaces.authentication_interface import AuthenticationInterface
from app.utils.query import exec_exists


async def auth_middleware(
    req: Request,
    auth_client: Annotated[AuthenticationInterface, Depends(get_auth_client_instance)],
):
    authorization = req.headers.get("Authorization")
    if not authorization:
        raise NoAuthorizationHeader()

    token = authorization.replace("Bearer ", "")
    resp = auth_client.verifyToken(token)

    db = next(db_client.get_session())
    exists = exec_exists(db, account_by_id(db, resp["sub"]))

    if not exists:
        raise AccountDoesNotExists()

    ownerid = req.path_params.get("ownerid", None)
    if ownerid and ownerid != resp["sub"]:
        raise IndentityMismatch()
