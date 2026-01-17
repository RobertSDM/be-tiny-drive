from sqlalchemy.orm import Session


from app.database.repositories.file_repo import (
    file_delete,
)
from app.features.file.utils import delete_file_from_storage, file_exists_or_raise
from app.utils.utils import make_file_bucket_path


class FileDeleteService:

    def delete_items(self, db: Session, ownerid: str, files: list[str]):
        for fileid in files:
            try:
                file = file_exists_or_raise(db, ownerid, fileid)

                delete_file_from_storage(
                    make_file_bucket_path(ownerid, fileid, "file"),
                    make_file_bucket_path(ownerid, fileid, "preview"),
                )

                file_delete(db, file)
            except:
                continue
