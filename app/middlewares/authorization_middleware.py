from fastapi import Request
import re

from app.core.exceptions import (
    AccountNotExists,
    DomainError,
    NoAuthorizationHeader,
    AccountMismatch,
)
from app.core.constants import non_protected_routes
from app.lib.supabase.authentication import supa_authentication


async def authorization_middleware(
    req: Request,
):
    for r in non_protected_routes:
        if re.match(r, req.url.path) is not None:
            return

    authorization = req.headers.get("Authorization")
    if not authorization:
        raise NoAuthorizationHeader()

    token = authorization.replace("Bearer ", "")
    data = supa_authentication.get_token_data(token)

    if not data:
        raise DomainError("The JWT Token is invalid", 422)

    ownerid = req.path_params.get("ownerid")
    if ownerid and ownerid != data.id:
        raise AccountMismatch()

    req.state.owner = data
