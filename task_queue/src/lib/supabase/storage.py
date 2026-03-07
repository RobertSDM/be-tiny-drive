from storage3 import SyncStorageClient
from supabase import create_client

from task_queue.src.constants import SUPA_KEY, SUPA_URL


class SupabaseStorageService:
    def __init__(self, client: SyncStorageClient) -> None:
        self._storage: SyncStorageClient = client

    def save(self, bucketid: str, content_type: str, path: str, file: bytes):
        self._storage.from_(bucketid).upload(path, file, {"content-type": content_type})

    def download(self, bucketid, fileid) -> bytes:
        return self._storage.from_(bucketid).download(fileid)


supabase_storage_client = SupabaseStorageService(create_client(SUPA_URL, SUPA_KEY).storage)
