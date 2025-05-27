from app.enums.enums import Mode
from app.features.auth.client.mock_auth_client import MockAuthenticationClient
from app.features.auth.client.supabase_auth_client import SupabaseAuthenticationClient
from app.interfaces.authentication_interface import AuthenticationInterface
from app.constants.env import mode, supabase_key, supabase_url


def get_auth_client_instance() -> AuthenticationInterface:
    if mode == Mode.PROD:
        return SupabaseAuthenticationClient(supabase_url, supabase_key)
    else:
        return MockAuthenticationClient()
