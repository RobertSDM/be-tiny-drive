from abc import ABC, abstractmethod
from typing import Optional

from app.core.schemas import RegisterPassword


class AuthenticationInterface(ABC):
    @abstractmethod
    def registerPassword(self, email: str, password: str) -> Optional[RegisterPassword]:
        raise NotImplementedError()
