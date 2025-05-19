from fastapi import Request
from jose import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from app.constants.env_ import jwt_secret

from app.core.exceptions import InvalidJWTToken, JWTTokenExpired, NoAuthorizationHeader


async def auth_middleware(req: Request):
    authorization = req.headers.get("Authorization")
    if not authorization:
        raise NoAuthorizationHeader()

    token = authorization.replace("Bearer ", "")
    try:
        jwt.decode(token, jwt_secret, algorithms="HS256", audience="authenticated")
    except InvalidTokenError:
        raise InvalidJWTToken()
    except ExpiredSignatureError:
        raise JWTTokenExpired()
