from abc import ABC, abstractmethod
from typing import Generator
from sqlalchemy.orm import Session

class DatabaseClientInterface(ABC):
    @abstractmethod
    def get_session(self) -> Generator[Session, None, None]:
        raise NotImplementedError()
