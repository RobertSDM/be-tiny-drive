from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.authentication_client_singleton import get_auth_service
from app.core.exceptions import (
    AccountNotExists,
    NoAuthorizationHeader,
    IndentityMismatch,
)
from app.core.non_protected_routes import routes
from app.lib.sqlalchemy import client
from app.database.repositories.account_repo import account_by_id
from app.interfaces.authentication_interface import AuthenticationInterface


async def authorization_middleware(
    req: Request,
    auth_client: AuthenticationInterface = Depends(get_auth_service),
):
    for r in routes:
        if req.url.path.startswith("/" + r):
            return

    authorization = req.headers.get("Authorization")
    if not authorization:
        raise NoAuthorizationHeader()

    token = authorization.replace("Bearer ", "")
    data = auth_client.get_token_data(token)

    if not data:
        raise AccountNotExists()

    ownerid = req.path_params.get("ownerid")
    if ownerid and ownerid != data.id:
        raise IndentityMismatch()

    req.state.owner = data
