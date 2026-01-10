from storage3 import SyncStorageClient
from supabase import create_client
from app.core.constants import SUPA_KEY, SUPA_URL


class SupabaseStorageClient:
    def __init__(self, url: str, key: str):
        self.sustorage: SyncStorageClient = create_client(url, key).storage

    def save(self, bucketid: str, content_type: str, path: str, file: bytes):
        return self.sustorage.from_(bucketid).upload(
            path, file, {"content-type": content_type}
        )

    def remove(self, bucketid: str, fileid: str):
        return self.sustorage.from_(bucketid).remove(fileid)

    def download(self, bucketid, fileid) -> bytes:
        return self.sustorage.from_(bucketid).download(fileid)

    def signedURL(
        self, buckedid: int, fileid: int, expires_in: int, download: str | bool = False
    ) -> str:
        return self.sustorage.from_(buckedid).create_signed_url(
            fileid, expires_in, {"download": download}
        )["signedUrl"]


supabase_storage_client = SupabaseStorageClient(SUPA_URL, SUPA_KEY)
