from supabase import create_client
from app.interfaces.authentication_interface import AuthenticationInterface
from app.constants.env import supabase_url, supabase_key


class SupabaseAuthClient(AuthenticationInterface):
    def __init__(self, url: str, key: str):
        self.suauth = create_client(url, key).auth

    def registerPassword(self, email: str, password: str):
        return self.suauth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )


auth_client = SupabaseAuthClient(supabase_url, supabase_key)
