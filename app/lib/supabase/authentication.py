from typing import Any, Optional
from jose import ExpiredSignatureError, JWTError, jwt
from supabase import create_client
from app.core.exceptions import InvalidJWTToken, JWTTokenExpired
from app.core.schemas import AccountDTO, LoginData
from app.interfaces.authentication_interface import (
    AuthenticationInterface,
)
from app.core.constants import JWT_SECRET


class SupabaseAuthenticationClient(AuthenticationInterface):
    def __init__(self, url: str, key: str):
        self.suauth = create_client(url, key).auth

    def register(
        self, email: str, password: str, username: str
    ) -> Optional[AccountDTO]:
        resp = self.suauth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": {"username": username}},
            }
        )

        if not resp.user:
            return None

        return AccountDTO(
            id=resp.user.id,
            created_at=resp.user.created_at,
            email=resp.user.email,
        )

    def login(self, email: str, password: str) -> Optional[LoginData]:
        resp = self.suauth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        if not resp.user:
            return None

        return LoginData(
            access_token=resp.session.access_token,
            refresh_token=resp.session.refresh_token,
            user=AccountDTO(
                id=resp.user.id,
                created_at=resp.user.created_at,
                email=resp.user.email,
                username="",
            ),
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
