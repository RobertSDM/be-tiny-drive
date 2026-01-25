from abc import ABC, abstractmethod
from typing import Optional

from app.core.schemas import AccountDTO, LoginData


class AuthenticationInterface(ABC):
    @abstractmethod
    def register(
        self, email: str, password: str, username: str
    ) -> Optional[AccountDTO]: ...

    @abstractmethod
    def delete(self, id_: str) -> None: ...

    @abstractmethod
    def login(self, email: str, password: str) -> Optional[LoginData]: ...

    @abstractmethod
    def logout(self, jwt: str) -> bool: ...

    @abstractmethod
    def get_token_data(self, token: str) -> Optional[AccountDTO]: ...
