from abc import ABC, abstractmethod
from typing import Any, Optional

from app.core.schemas import RegisterPassword


class AuthenticationInterface(ABC):
    @abstractmethod
    def registerPassword(self, email: str, password: str) -> Optional[RegisterPassword]:
        raise NotImplementedError()

    @abstractmethod
    def validateToken(self, token: str) -> dict[str, Any]:
        raise NotImplementedError()
