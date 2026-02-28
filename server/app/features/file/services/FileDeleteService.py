from typing import List
from sqlalchemy.orm import Session
from storage3.exceptions import StorageApiError

from server.app.core.constants import SUPA_BUCKETID, SUPPORTED_IMAGE_PREVIEW_TYPES
from server.app.core.exceptions import FileNotFound
from server.app.lib.supabase.storage import supabase_storage_client
from server.app.database.models import FileModel
from server.app.database.repositories.file_repo import (
    file_by_ownerid_parentid,
    file_delete,
)
from server.app.features.file.utils import (
    get_file_or_raise,
)
from server.app.utils.utils import make_file_bucket_path


class FileDeleteService:

    def _cascade_storage(self, db: Session, ownerid: str, id_: str):
        """
        Remove the files data from the storage
        """

        files = file_by_ownerid_parentid(db, ownerid, id_).all()
        for file in files:
            if file.is_dir:
                self._cascade_storage(db, ownerid, file.id)
            else:
                self._move_to_trash(ownerid, file.id, file.content_type)

    def _move_from_trash(self, ownerid: str, fileid: str, content_type: str):
        supabase_storage_client.move(
            SUPA_BUCKETID,
            make_file_bucket_path(ownerid, fileid, "trash+file"),
            make_file_bucket_path(ownerid, fileid, "file"),
        )

        if content_type in SUPPORTED_IMAGE_PREVIEW_TYPES:
            supabase_storage_client.move(
                SUPA_BUCKETID,
                make_file_bucket_path(ownerid, fileid, "trash+preview"),
                make_file_bucket_path(ownerid, fileid, "preview"),
            )

    def _move_to_trash(self, ownerid: str, fileid: str, content_type: str):
        supabase_storage_client.move(
            SUPA_BUCKETID,
            make_file_bucket_path(ownerid, fileid, "file"),
            make_file_bucket_path(ownerid, fileid, "trash+file"),
        )

        if content_type in SUPPORTED_IMAGE_PREVIEW_TYPES:
            supabase_storage_client.move(
                SUPA_BUCKETID,
                make_file_bucket_path(ownerid, fileid, "preview"),
                make_file_bucket_path(ownerid, fileid, "trash+preview"),
            )

    def delete_files(
        self, db: Session, ownerid: str, fileids: List[str]
    ) -> List[FileModel]:
        files = list()

        try:
            for fileid in fileids:
                file = get_file_or_raise(db, ownerid, fileid)
                files.append(file)


                if file.is_dir:
                    self._cascade_storage(db, ownerid, file.id)
                else:
                    self._move_to_trash(ownerid, file.id, file.content_type)

                file_delete(db, file)
        except StorageApiError as e:
            for file in files:
                self._move_from_trash(ownerid, file.id, file.content_type)

            if e.code == "NoSuchUpload":
                raise FileNotFound()

            raise e
        except Exception as e:
            for file in files:
                self._move_from_trash(ownerid, file.id, file.content_type)

            raise e

        return files
