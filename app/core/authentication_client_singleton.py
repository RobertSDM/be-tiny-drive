from app.core.schemas import Mode
from app.features.auth.client.mock_auth_client import MockAuthenticationClient
from app.lib.supabase.authentication import SupabaseAuthenticationClient
from app.interfaces.authentication_interface import AuthenticationInterface
from app.core.constants import MODE, SUPA_KEY, SUPA_URL


class AuthClientSingleton:
    _instance = None

    @staticmethod
    def get_instance() -> AuthenticationInterface:
        if not AuthClientSingleton._instance:
            if MODE == Mode.PROD.value:
                AuthClientSingleton._instance = SupabaseAuthenticationClient(
                    SUPA_URL, SUPA_KEY
                )
            else:
                AuthClientSingleton._instance = MockAuthenticationClient()

        return AuthClientSingleton._instance
