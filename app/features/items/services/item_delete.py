from sqlalchemy.orm import Session
import storage3
import storage3.exceptions

from app.core.exceptions import ItemNotFound
from app.features.storage.supabase_storage_client import (
    supabase_storage_client as storage_client,
)

from app.database.models import Item
from app.database.repositories.item_repo import (
    item_by_id_ownerid,
    item_by_ownerid_parentid,
    item_delete,
)
from app.constants.env import drive_bucketid
from app.enums.enums import ItemType
from app.utils.query import (
    exec_all,
    exec_first,
    update,
)
from app.database.repositories.item_repo import item_delete
from app.utils.utils import make_bucket_file_path, make_bucket_file_preview_path


class _ItemDeleteServ:

    # def _delete_item_from_storage(self, item: Item) -> bool:
    #     try:
    #         storage_client.remove(
    #             drive_bucketid,
    #             make_bucket_file_path(item),
    #         )

    #         storage_client.remove(
    #             drive_bucketid,
    #             make_bucket_file_preview_path(item),
    #         )

    #         return True
    #     except storage3.exceptions.StorageApiError as e:
    #         match e.code:
    #             case "NoSuchUpload":
    #                 raise ItemNotFound()

    #         return False

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

    def delete_items_serv(
        self, db: Session, ownerid: str, items: list[str]
    ) -> list[str]:
        deleted = []

        for id in items:
            item = exec_first(item_by_id_ownerid(db, id, ownerid))

            if not item:
                continue

            if item.type == ItemType.FOLDER:
                children = exec_all(item_by_ownerid_parentid(db, ownerid, id))
                children = [c.id for c in children]
                self.delete_items_serv(db, ownerid, children)

            update(item_by_id_ownerid(db, id, ownerid), {"to_delete": True})

            deleted.append(id)

        return deleted


item_delete_serv = _ItemDeleteServ()
