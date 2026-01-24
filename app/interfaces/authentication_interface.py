from abc import ABC, abstractmethod
from typing import Any, Optional

from app.core.schemas import AccountDTO, LoginData


class AuthenticationInterface(ABC):
    @abstractmethod
    def register(
        self, email: str, password: str, username: str
    ) -> Optional[AccountDTO]:
        pass

    @abstractmethod
    def login(self, email, password: str) -> Optional[LoginData]:
        pass

    @abstractmethod
    def validateToken(self, token: str) -> dict[str, Any]:
        pass
