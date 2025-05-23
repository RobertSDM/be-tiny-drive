from sqlalchemy.orm import Session

from app.clients.supabase.storage_client import storage

from app.database.models import Item
from app.database.repositories.item_repo import (
    item_by_id_ownerid,
    item_by_ownerid_parentid,
    item_delete,
)
from app.constants.env_ import drive_bucketid
from app.enums.enums import ItemType
from app.utils.execute_query import (
    execute_all,
    execute_first,
)
from app.utils.utils import make_bucket_path


def _delete_item_from_storage(item: Item) -> bool:
    try:
        storage.remove(
            drive_bucketid,
            make_bucket_path(item),
        )
        return True
    except:
        return False


def _dfs_delete_items(
    db: Session,
    children: list[Item],
    ownerid: str,
    successes: list[str],
    failures: list[str],
):
    for c in children:
        if c.type == ItemType.FOLDER:
            children = execute_all(item_by_ownerid_parentid(db, ownerid, c.id))
            _dfs_delete_items(db, children, ownerid, successes, failures)
        else:
            if _delete_item_from_storage(c):
                successes.append(c.id)
            else:
                failures.append(c.id)


def delete_items_serv(
    db: Session, ownerid: str, items: list[str]
) -> tuple[list[str], list[str]]:
    successes = list()
    failures = list()

    for id in items:
        item = execute_first(item_by_id_ownerid(db, id, ownerid))

        if not item:
            failures.append(id)
            continue

        if item.type == ItemType.FOLDER:
            items = execute_all(item_by_ownerid_parentid(db, ownerid, item.id))
            _dfs_delete_items(db, items, ownerid, successes, failures)
            successes.append(item.id)
        else:
            if _delete_item_from_storage(item):
                successes.append(id)
            else:
                failures.append(id)

        item_delete(db, item)

    return successes, failures
