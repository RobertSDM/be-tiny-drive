from typing import List, Optional
from sqlalchemy.orm import Session


from app.database.repositories.file_repo import (
    file_by_ownerid_parentid,
    file_delete,
)
from app.features.file.utils import delete_file_from_storage, get_file_or_raise
from app.utils.utils import make_file_bucket_path


class FileDeleteService:

    def _cascade_storage(self, db: Session, ownerid: str, id_: str):
        files = file_by_ownerid_parentid(db, ownerid, id_).all()
        for file in files:
            if file.is_dir:
                self._cascade_storage(db, ownerid, file.id)
            else:
                previewid: Optional[str] = None
                if file.content_type.startswith("image"):
                    previewid = make_file_bucket_path(ownerid, file.id, "preview")

                delete_file_from_storage(
                    make_file_bucket_path(ownerid, file.id, "file"),
                    previewid,
                )

    def delete_files(self, db: Session, ownerid: str, files: List[str]):
        for fileid in files:
            file = get_file_or_raise(db, ownerid, fileid)

            if file.is_dir:
                self._cascade_storage(db, ownerid, file.id)
            else:
                previewid: Optional[str] = None
                if file.content_type.startswith("image"):
                    previewid = make_file_bucket_path(ownerid, file.id, "preview")

                delete_file_from_storage(
                    make_file_bucket_path(ownerid, file.id, "file"),
                    previewid,
                )

            file_delete(db, file)
