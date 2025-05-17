from typing import Optional
from sqlalchemy.orm import Session

from app.core.exeptions import (
    ItemDeleteError,
    ItemExistsInFolder,
    ItemNotFound,
    ParentFolderNotFound,
)
from app.database.models import Item
from app.database.repositories import (
    item_save,
    item_by_ownerid_parentid,
    item_by_id,
    item_by_id_ownerid,
    item_by_id_type,
    item_by_ownerid_parentid_path,
    item_delete,
)
from app.utils.enums import ItemType
from app.utils.execute_query import (
    execute_all,
    execute_exists,
    execute_first,
    update_entity,
)
from app.utils import get_sufix_to_bytes


def item_create_serv(
    db: Session,
    name: str,
    parentid: str | None,
    extension: str,
    size: int,
    data: bytes,
    ownerid: str,
    path: str,
    type: ItemType,
) -> Item:
    fmtsize, prefix = get_sufix_to_bytes(size)

    if parentid == "":
        parentid = None

    item_exists = execute_exists(
        db, item_by_ownerid_parentid_path(db, ownerid, parentid, path)
    )

    if item_exists:
        raise ItemExistsInFolder(name, type.value)

    if parentid:
        parent_exists = execute_exists(
            db, item_by_id_type(db, parentid, ItemType.FOLDER.value)
        )

        if not parent_exists:
            raise ParentFolderNotFound()

    item = Item(
        name=name,
        data=data,
        extension=extension,
        size=fmtsize,
        size_prefix=prefix,
        ownerid=ownerid,
        path=path,
        parentid=parentid,
        type=type,
    )

    return item_save(db, item)


def item_update_name(db: Session, id: str, name: str) -> Item:
    query = item_by_id(db, id)
    item = execute_first(query)
    if not item:
        raise ItemNotFound

    update_entity(query, {Item.name: name})
    db.commit()
    return item


def all_root_items_serv(db: Session, ownerid: str) -> list[Item]:
    return execute_all(item_by_ownerid_parentid(db, ownerid, None))


def item_by_id_serv(db: Session, ownerid: str, id: str):
    item = execute_first(item_by_id_ownerid(db, id, ownerid))

    if not item:
        raise ItemNotFound

    return item


def all_items_in_folder_serv(db: Session, ownerid: str, parentid: Optional[str]):
    items = execute_all(item_by_ownerid_parentid(db, ownerid, parentid))
    return items


def delete_item_serv(db: Session, ownerid: str, id: str) -> Item:
    item = execute_first(item_by_id_ownerid(db, id, ownerid))

    if not item:
        raise ItemNotFound()

    item_delete(db, item)

    return item


# def download_serv(db, id, owner_id):
#     data = download_file(db, id, owner_id)
#     # byte_data = get_bytes_data()
#     return [data, data.fileData.byteData]
