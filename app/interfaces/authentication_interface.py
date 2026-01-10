from abc import ABC, abstractmethod
from typing import Any, Optional

from app.core.schemas import AccountReturnable


class AuthenticationInterface(ABC):
    @abstractmethod
    def AccountReturnable(
        self, email: str, password: str
    ) -> Optional[AccountReturnable]:
        raise NotImplementedError()

    @abstractmethod
    def validateToken(self, token: str) -> dict[str, Any]:
        raise NotImplementedError()
