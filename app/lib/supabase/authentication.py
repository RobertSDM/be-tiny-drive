from typing import Any, Optional
from jose import ExpiredSignatureError, JWTError, jwt
from supabase import create_client
from app.core.exceptions import InvalidJWTToken, JWTTokenExpired
from app.core.schemas import AccountReturnable
from app.interfaces.authentication_interface import (
    AuthenticationInterface,
)
from app.core.constants import JWT_SECRET


class SupabaseAuthenticationClient(AuthenticationInterface):
    def __init__(self, url: str, key: str):
        self.suauth = create_client(url, key).auth

    def AccountReturnable(
        self, email: str, password: str
    ) -> Optional[AccountReturnable]:
        resp = self.suauth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

        if not resp.user:
            return None

        return AccountReturnable(
            id=resp.user.id, creation_date=resp.user.created_at, email=resp.user.email
        )

    def validateToken(self, token: str) -> dict[str, Any]:
        try:
            resp = jwt.decode(
                token, JWT_SECRET, algorithms="HS256", audience="authenticated"
            )
            return resp
        except JWTError:
            raise InvalidJWTToken()
        except ExpiredSignatureError:
            raise JWTTokenExpired()
