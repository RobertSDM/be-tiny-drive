from typing import Any
from app.core.schemas import AccountReturnable
from app.interfaces.authentication_interface import AuthenticationInterface


class MockAuthenticationClient(AuthenticationInterface):
    def AccountReturnable(self, email, password) -> AccountReturnable:
        return AccountReturnable(
            id="3acd40a6-f384-4e34-8f95-476a0dec91a6",
            creation_date="2025-05-27T13:51:34.116Z",
            email="test@gmail.com",
            username="testingok?",
        )

    def validateToken(self, token) -> dict[str, Any]:
        return {"sub": "3acd40a6-f384-4e34-8f95-476a0dec91a6"}
