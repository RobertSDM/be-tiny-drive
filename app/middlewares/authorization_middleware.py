from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AccountNotExists,
    NoAuthorizationHeader,
    IndentityMismatch,
)
from app.core.authentication_client_singleton import AuthClientSingleton
from app.lib.sqlalchemy import client
from app.database.repositories.account_repo import account_by_id
from app.interfaces.authentication_interface import AuthenticationInterface


async def authorization_middleware(
    req: Request,
    auth_client: AuthenticationInterface = Depends(AuthClientSingleton.get_instance),
    db: Session = Depends(client.get_session),
):
    authorization = req.headers.get("Authorization")
    if not authorization:
        raise NoAuthorizationHeader()

    token = authorization.replace("Bearer ", "")
    tokenValue = auth_client.validateToken(token)

    exists = account_by_id(db, tokenValue["sub"]).first()

    if not exists:
        raise AccountNotExists()

    ownerid = req.path_params.get("ownerid")
    if ownerid and ownerid != tokenValue["sub"]:
        raise IndentityMismatch()
