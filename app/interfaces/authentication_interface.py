from abc import ABC, abstractmethod


class AuthenticationInterface(ABC):
    @abstractmethod
    def register(self, email: str, password: str):
        raise NotImplementedError()