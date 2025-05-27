from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageClientInterface(ABC):
    @abstractmethod
    def save(self, bucketid: str, content_type: str, file: BinaryIO):
        raise NotImplementedError()

    @abstractmethod
    def remove(self, bucketid: str, fileid: str):
        raise NotImplementedError()

    @abstractmethod
    def update(self, bucketid: str, fileid: str):
        raise NotImplementedError()

    @abstractmethod
    def get(self, bucketid: str, fileid: str):
        raise NotImplementedError()

    @abstractmethod
    def download(self, bucketid: str, fileid: str) -> BinaryIO:
        raise NotImplementedError()

    @abstractmethod
    def list(self, buckedid: str, path: str) -> list[dict[str, any]]:
        raise NotImplementedError()

    @abstractmethod
    def signedURL(self, buckedid: str, fileid: str, expire_in: int):
        raise NotImplementedError()
