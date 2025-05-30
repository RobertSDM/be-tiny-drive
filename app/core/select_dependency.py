from app.enums.enums import Mode
from app.features.auth.client.mock_auth_client import MockAuthenticationClient
from app.features.auth.client.supabase_auth_client import SupabaseAuthenticationClient
from app.interfaces.authentication_interface import AuthenticationInterface
from app.constants.env import mode, supabase_key, supabase_url


class AuthClientSingleton:
    _instance = None

    @staticmethod
    def get_instance() -> AuthenticationInterface:
        if not AuthClientSingleton._instance:
            if mode == Mode.PROD.value:
                AuthClientSingleton._instance = SupabaseAuthenticationClient(
                    supabase_url, supabase_key
                )
            else:
                AuthClientSingleton._instance = MockAuthenticationClient()

        return AuthClientSingleton._instance
