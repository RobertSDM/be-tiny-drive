from typing import Callable
from storage3 import SyncStorageClient
from supabase import create_client
from app.utils.logging_config import logger
import httpx

from app.core.constants import SUPA_KEY, SUPA_URL


class SupabaseStorageClient:
    def __init__(self, url: str, key: str):
        self._url = url
        self._key = key
        self._storage: SyncStorageClient = self._new_client()
        self._max_retries = 2

    def _new_client(self) -> SyncStorageClient:
        return create_client(self._url, self._key).storage

    def _run_and_retry(self, func: Callable[[], None]):
        for retry in range(self._max_retries):
            try:
                return func()
            except httpx.RemoteProtocolError:
                if retry < self._max_retries - 1:
                    logger.info("Recreating the storage client")
                    self._storage = self._new_client()
                else:
                    raise

    def save(self, bucketid: str, content_type: str, path: str, file: bytes):
        return self._run_and_retry(
            lambda: self._storage.from_(bucketid).upload(
                path, file, {"content-type": content_type}
            )
        )

    def remove(self, bucketid: str, fileid: str):
        return self._run_and_retry(lambda: self._storage.from_(bucketid).remove(fileid))

    def download(self, bucketid, fileid) -> bytes:
        return self._run_and_retry(
            lambda: self._storage.from_(bucketid).download(fileid)
        )

    def move(self, bucketid: str, from_: str, to: str):
        self._run_and_retry(lambda: self._storage.from_(bucketid).move(from_, to))

    def signedURL(
        self, buckedid: int, fileid: int, expires_in: int, download: str | bool = False
    ) -> str:
        return self._run_and_retry(
            lambda: self._storage.from_(buckedid).create_signed_url(
                fileid, expires_in, {"download": download}
            )["signedUrl"]
        )


supabase_storage_client = SupabaseStorageClient(SUPA_URL, SUPA_KEY)
