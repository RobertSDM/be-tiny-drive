from typing import Optional
from gotrue.errors import AuthApiError
from supabase import create_client
from gotrue.types import UserResponse

from app.core.constants import SUPA_KEY, SUPA_URL
from app.core.schemas import AccountDTO, LoginData, RefreshSessionData
from app.core.interfaces.AuthenticationInterface import AuthenticationInterface


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
            username=username,
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

    def logout(self, jwt: str) -> bool:
        try:
            self.suauth.admin.sign_out(
                jwt,
            )
            return True
        except AuthApiError:
            return False

    def refresh(self, token) -> Optional[RefreshSessionData]:
        resp = self.suauth.refresh_session(token)

        if not resp.user:
            return None

        return RefreshSessionData(
            access_token=resp.session.access_token,
            refresh_token=resp.session.refresh_token,
        )

    def get_token_data(self, token: str) -> Optional[UserResponse]:
        try:
            user = self.suauth.get_user(token)

            return AccountDTO(
                created_at=user.user.created_at,
                email=user.user.email,
                username=user.user.user_metadata["username"],
                id=user.user.id,
            )
        except AuthApiError:
            return None

    def delete(self, id_):
        self.suauth.admin.delete_user(id_)


supa_authentication = SupabaseAuthenticationClient(SUPA_URL, SUPA_KEY)
