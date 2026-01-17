from sqlalchemy import update
from sqlalchemy.orm import Session


from app.core.exceptions import FileNotFound, NotFound
from app.database.models import FileModel
from app.database.repositories.item_repo import (
    file_by_id_ownerid,
    file_by_id_ownerid_active,
)
from app.features.file.utils import delete_file_from_storage, file_exists_or_raise
from app.utils.utils import make_file_bucket_path


class FileDeleteService:

    def delete_items(self, db: Session, ownerid: str, files: list[str]):
        for fileid in files:
            try:
                file_exists_or_raise(db, ownerid, fileid)
            except:
                continue

            delete_file_from_storage(
                make_file_bucket_path(ownerid, fileid, "file"),
                make_file_bucket_path(ownerid, fileid, "preview"),
            )

            db.execute(
                update(FileModel)
                .filter(
                    FileModel.ownerid == ownerid,
                    FileModel.id == fileid,
                    FileModel.to_delete.is_(False),
                )
                .values({"to_delete": True})
            )
