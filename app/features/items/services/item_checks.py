from pytest import Session

from app.core.exceptions import ItemExistsInFolder, ParentFolderNotFound
from app.database.repositories.item_repo import (
    item_by_id_ownerid,
    item_by_ownerid_parentid_fullname_non_deleted,
)
from app.enums.enums import ItemType
from app.utils.query import exec_exists


class _ItemChecks:

    def check_duplicate_name(
        self,
        db: Session,
        ownerid: str,
        parentid: str | None,
        filename: str,
        type: ItemType,
    ) -> None:
        name = filename.split("/")[-1]
        exists = exec_exists(
            db,
            item_by_ownerid_parentid_fullname_non_deleted(db, ownerid, parentid, name),
        )
        if exists:
            raise ItemExistsInFolder(name, type.value)

    def check_parent_exists(self, db: Session, ownerid: str, parentid: str | None):
        if not parentid:
            return

        exists = exec_exists(db, item_by_id_ownerid(db, parentid, ownerid))
        if not exists:
            raise ParentFolderNotFound()


item_checks = _ItemChecks()
