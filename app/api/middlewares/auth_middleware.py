from fastapi import Request
from jose import jwt
from jwt import InvalidTokenError, ExpiredSignatureError

from app.core.exceptions import (
    AccountDoesNotExists,
    InvalidJWTToken,
    JWTTokenExpired,
    NoAuthorizationHeader,
    WrongIdentityJWTToken,
)
from app.constants.env_ import jwt_secret
from app.clients.sqlalchemy_client import db_client
from app.database.repositories.account_repo import account_by_id
from app.database.repositories.item_repo import item_by_id_ownerid
from app.utils.execute_query import execute_exists


async def auth_middleware(req: Request):
    authorization = req.headers.get("Authorization")
    if not authorization:
        raise NoAuthorizationHeader()

    token = authorization.replace("Bearer ", "")
    try:
        resp = jwt.decode(
            token, jwt_secret, algorithms="HS256", audience="authenticated"
        )

        db = next(db_client.get_session())
        exists = execute_exists(db, account_by_id(db, resp["sub"]))

        if not exists:
            raise AccountDoesNotExists()

        ownerid = req.path_params.get("ownerid", None)
        if ownerid and ownerid != resp["sub"]:
            raise WrongIdentityJWTToken()

    except InvalidTokenError:
        raise InvalidJWTToken()
    except ExpiredSignatureError:
        raise JWTTokenExpired()
