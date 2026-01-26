from typing import List
from sqlalchemy.orm import Session
from storage3.exceptions import StorageApiError

from app.core.constants import SUPA_BUCKETID
from app.core.exceptions import FileNotFound
from app.lib.supabase.storage import supabase_storage_client
from app.database.models import FileModel
from app.database.repositories.file_repo import (
    file_by_ownerid_parentid,
    file_delete,
)
from app.features.file.utils import (
    get_file_or_raise,
)
from app.utils.utils import make_file_bucket_path


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
                self._move_to_trash(ownerid, file)

    def _move_from_trash(self, ownerid: str, file: FileModel):
        supabase_storage_client.move(
            SUPA_BUCKETID,
            make_file_bucket_path(ownerid, file.id, "trash+file"),
            make_file_bucket_path(ownerid, file.id, "file"),
        )

        if file.content_type.startswith("image"):
            supabase_storage_client.move(
                SUPA_BUCKETID,
                make_file_bucket_path(ownerid, file.id, "trash+preview"),
                make_file_bucket_path(ownerid, file.id, "preview"),
            )

    def _move_to_trash(self, ownerid: str, file: FileModel):
        supabase_storage_client.move(
            SUPA_BUCKETID,
            make_file_bucket_path(ownerid, file.id, "file"),
            make_file_bucket_path(ownerid, file.id, "trash+file"),
        )

        if file.content_type.startswith("image"):
            supabase_storage_client.move(
                SUPA_BUCKETID,
                make_file_bucket_path(ownerid, file.id, "preview"),
                make_file_bucket_path(ownerid, file.id, "trash+preview"),
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
                    self._move_to_trash(ownerid, file)

                file_delete(db, file)
        except StorageApiError as e:
            for file in files:
                self._move_from_trash(ownerid, file)

            if e.code == "NoSuchUpload":
                raise FileNotFound()

            raise e
        except Exception as e:
            for file in files:
                self._move_from_trash(ownerid, file)

            raise e

        return files
