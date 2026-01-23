from typing import Any
from app.core.schemas import AccountReturnable
from app.interfaces.authentication_interface import AuthenticationInterface


class MockAuthenticationClient(AuthenticationInterface):
    def AccountReturnable(self, email, password) -> AccountReturnable:
        return AccountReturnable(
            id="7dc334cc-c103-4bd4-bdf4-dfc2a76f2f2d",
            creation_date="2025-05-27T13:51:34.116Z",
            email="test@gmail.com",
            username="testingok?",
        )

    def validateToken(self, token) -> dict[str, Any]:
        return {"sub": "7dc334cc-c103-4bd4-bdf4-dfc2a76f2f2d"}
