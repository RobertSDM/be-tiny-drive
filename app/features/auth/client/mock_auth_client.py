from typing import Any, Optional
from app.core.schemas import AccountDTO, LoginData
from app.interfaces.authentication_interface import AuthenticationInterface


class MockAuthenticationClient(AuthenticationInterface):
    def register(self, email, password) -> AccountDTO:
        return AccountDTO(
            id="7dc334cc-c103-4bd4-bdf4-dfc2a76f2f2d",
            creation_date="2025-05-27T13:51:34.116Z",
            email="test@gmail.com",
            username="testingok?",
        )

    def login(self, email, password) -> Optional[LoginData]:
        return LoginData(
            access_token="",
            refresh_token="",
            user=AccountDTO(
                id="7dc334cc-c103-4bd4-bdf4-dfc2a76f2f2d",
                created_at="2025-05-27T13:51:34.116Z",
                email="test@gmail.com",
                username="testingok",
            ),
        )

    def get_token_data(self, token) -> dict[str, Any]:
        return {"sub": "7dc334cc-c103-4bd4-bdf4-dfc2a76f2f2d"}
