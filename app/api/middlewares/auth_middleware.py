from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from jose import jwt
from app.constants.env_definitions import jwt_secret

from app.core.exeptions import InvalidJWTToken, JWTTokenExpired, NoAuthenticationHeader


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, req: Request, call_next: RequestResponseEndpoint):
        authorization = req.headers.get("Authorization")
        if not authorization:
            raise NoAuthenticationHeader()

        token = authorization.replace("Bearer ", "")
        try:
            jwt.decode(token, jwt_secret, "HS256", "authenticated")
        except jwt.InvalidTokenError:
            raise InvalidJWTToken()
        except jwt.ExpiredSignatureError:
            raise JWTTokenExpired()

        return await call_next(req)
