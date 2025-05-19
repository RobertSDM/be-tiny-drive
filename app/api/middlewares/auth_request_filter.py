from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from jose import jwt
from app.constants.env_ import jwt_secret

from app.core.exceptions import InvalidJWTToken, JWTTokenExpired, NoAuthorizationHeader


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, req: Request, call_next: RequestResponseEndpoint):
        authorization = req.headers.get("Authorization")
        if not authorization:
            raise NoAuthorizationHeader()

        token = authorization.replace("Bearer ", "")
        try:
            jwt.decode(token, jwt_secret, "HS256", "authenticated")
        except jwt.InvalidTokenError:
            raise InvalidJWTToken()
        except jwt.ExpiredSignatureError:
            raise JWTTokenExpired()

        return await call_next(req)
