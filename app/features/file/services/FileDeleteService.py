from sqlalchemy.orm import Session


from app.database.repositories.file_repo import (
    file_delete,
)
from app.features.file.utils import delete_file_from_storage, file_exists_or_raise, get_file_or_raise
from app.utils.utils import make_file_bucket_path


class FileDeleteService:

    def delete_files(self, db: Session, ownerid: str, files: list[str]):
        for fileid in files:
            file = get_file_or_raise(db, ownerid, fileid)

            file_delete(db, file)

            delete_file_from_storage(
                make_file_bucket_path(ownerid, fileid, "file"),
                make_file_bucket_path(ownerid, fileid, "preview"),
            )
