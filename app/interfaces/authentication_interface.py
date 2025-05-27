from abc import ABC, abstractmethod


class AuthenticationInterface(ABC):
    @abstractmethod
    def registerPassword(self, email: str, password: str):
        raise NotImplementedError()
