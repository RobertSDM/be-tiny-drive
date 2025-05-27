from typing import Optional
from supabase import create_client
from app.interfaces.authentication_interface import (
    AuthenticationInterface,
    RegisterPassword,
)
from app.constants.env import supabase_url, supabase_key


class SupabaseAuthClient(AuthenticationInterface):
    def __init__(self, url: str, key: str):
        self.suauth = create_client(url, key).auth

    def registerPassword(self, email: str, password: str) -> Optional[RegisterPassword]:
        resp = self.suauth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

        if not resp.user:
            return None

        return RegisterPassword(
            id=resp.user.id, creation_date=resp.user.created_at, email=resp.user.email
        )


supabase_auth_client = SupabaseAuthClient(supabase_url, supabase_key)
