from sqlalchemy.orm import Session

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
)
from app.database.repositories.item_repo import item_delete
from app.utils.utils import make_bucket_file_path


class _ItemDeleteServ:

    def _delete_item_from_storage(self, item: Item) -> bool:
        try:
            storage_client.remove(
                drive_bucketid,
                make_bucket_file_path(item),
            )
            return True
        except:
            return False

    def _dfs_delete_items(
        self,
        db: Session,
        children: list[Item],
        ownerid: str,
        successes: list[str],
        failures: list[str],
    ):
        for c in children:
            if c.type == ItemType.FOLDER:
                children = exec_all(item_by_ownerid_parentid(db, ownerid, c.id))
                self._dfs_delete_items(db, children, ownerid, successes, failures)
            else:
                if self._delete_item_from_storage(c):
                    successes.append(c.id)
                else:
                    failures.append(c.id)

    def delete_items_serv(
        self, db: Session, ownerid: str, items: list[str]
    ) -> tuple[list[str], list[str]]:
        successes = list()
        failures = list()

        for id in items:
            item = exec_first(item_by_id_ownerid(db, id, ownerid))

            if not item:
                failures.append(id)
                continue

            if item.type == ItemType.FOLDER:
                items = exec_all(item_by_ownerid_parentid(db, ownerid, item.id))
                self._dfs_delete_items(db, items, ownerid, successes, failures)
                successes.append(item.id)
            else:
                if self._delete_item_from_storage(item):
                    successes.append(id)
                else:
                    failures.append(id)

            item_delete(db, item)

        return successes, failures


item_delete_serv = _ItemDeleteServ()
