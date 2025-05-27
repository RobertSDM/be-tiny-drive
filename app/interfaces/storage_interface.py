from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageClientInterface(ABC):
    @abstractmethod
    def save(self, bucketid: str, content_type: str, file: BinaryIO):
        raise NotImplementedError()

    @abstractmethod
    def remove(self, bucketid: str, fileid: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def download(self, bucketid: str, fileid: str) -> BinaryIO:
        raise NotImplementedError()

    @abstractmethod
    def signedURL(self, buckedid: str, fileid: str, expire_in: int):
        raise NotImplementedError()
