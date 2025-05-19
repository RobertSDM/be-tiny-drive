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

    @abstractmethod
    def list(self, buckedid: str, path: str) -> list[dict[str, any]]:
        pass

    @abstractmethod
    def signedURL(self, buckedid: str, fileid: str, expire_in: int):
        pass
