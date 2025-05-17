from typing import BinaryIO
from storage3 import SyncStorageClient
from app.interfaces.storage_interface import StorageClientInterface
from supabase import create_client
from app.constants.env_definitions import supabase_key, supabase_url


class SupabaseStorageClient(StorageClientInterface):
    def __init__(self, url: str, key: str):
        self.storage: SyncStorageClient = create_client(url, key).storage

    def save(self, bucketid: str, content_type: str, path: str, file: BinaryIO) -> None:
        self.storage.from_(bucketid).upload(path, file, {"content-type": content_type})

    def remove(self, bucketid: str, fileid: str) -> None:
        self.storage.from_(bucketid).remove(fileid)

    def get(self, bucketid: str, fileid: str) -> str:
        data = self.storage.from_(bucketid).create_signed_url(fileid, 60)
        return data["signedURL"]

    def download(self, bucketid, fileid) -> bytes:
        return self.storage.from_(bucketid).download(fileid)


storage = SupabaseStorageClient(supabase_url, supabase_key)
