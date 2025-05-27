from abc import ABC, abstractmethod


class DatabaseClientInterface(ABC):
    @abstractmethod
    def get_session(self):
        raise NotImplementedError()
