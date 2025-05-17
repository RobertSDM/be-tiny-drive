from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageClientInterface(ABC):
    @abstractmethod
    def save(self, bucketid: str, content_type: str, file: BinaryIO):
        pass

    @abstractmethod
    def remove(self, bucketid: str, fileid: str):
        pass

    @abstractmethod
    def update(self, bucketid: str, fileid: str):
        pass

    @abstractmethod
    def get(self, bucketid: str, fileid: str):
        pass

    @abstractmethod
    def download(self, bucketid: str, fileid: str) -> BinaryIO:
        pass
