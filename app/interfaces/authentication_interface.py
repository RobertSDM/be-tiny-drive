from abc import ABC, abstractmethod
from typing import Optional

from app.core.schemas import AccountDTO, LoginData


class AuthenticationInterface(ABC):
    @abstractmethod
    def register(
        self, email: str, password: str, username: str
    ) -> Optional[AccountDTO]:
        pass

    @abstractmethod
    def logout(self, email: str) -> bool:
        pass

    @abstractmethod
    def login(self, email, password: str) -> Optional[LoginData]:
        pass

    @abstractmethod
    def get_token_data(self, token: str) -> Optional[AccountDTO]:
        pass
