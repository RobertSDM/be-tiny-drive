from sqlalchemy import update
from sqlalchemy.orm import Session


from app.core.exceptions import FileNotFound, NotFound
from app.database.models import FileModel
from app.database.repositories.item_repo import (
    file_by_id_ownerid,
    file_by_id_ownerid_active,
)
from app.features.file.utils import delete_file_from_storage
from app.utils.utils import make_file_bucket_path


class FileDeleteService:

    # def _dfs_delete_items(
    #     self,
    #     db: Session,
    #     children: list[Item],
    #     ownerid: str,
    #     successes: list[str],
    #     failures: list[str],
    # ):
    #     for c in children:
    #         if c.type == ItemType.FOLDER:
    #             children = exec_all(item_by_ownerid_parentid(db, ownerid, c.id))
    #             self._dfs_delete_items(db, children, ownerid, successes, failures)
    #         else:
    #             if self._delete_item_from_storage(c):
    #                 successes.append(c.id)
    #             else:
    #                 failures.append(c.id)

    def delete_items(self, db: Session, ownerid: str, files: list[str]):
        for fileid in files:
            exists = db.query(
                file_by_id_ownerid_active(db, fileid, ownerid).exists()
            ).scalar()

            if not exists:
                raise NotFound("Never existed or was already deleted")

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
