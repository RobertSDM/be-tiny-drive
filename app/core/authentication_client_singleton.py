from app.lib.supabase.authentication import SupabaseAuthenticationClient
from app.interfaces.authentication_interface import AuthenticationInterface
from app.core.constants import SUPA_KEY, SUPA_URL


def get_auth_service() -> AuthenticationInterface:
    # if MODE == Mode.value:
        return SupabaseAuthenticationClient(SUPA_URL, SUPA_KEY)
    # else:
        # return MockAuthenticationClient()
