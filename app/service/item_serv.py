from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.clients.supabase_storage_client import storage
from app.core.exeptions import (
    ItemNotFound,
)
from app.core.extract_metadata_file import create_file_structure
from app.database.models import Item
from app.database.repositories import (
    item_save,
    item_by_ownerid_parentid,
    item_by_id,
    item_by_id_ownerid,
    item_delete,
)
from app.utils.execute_query import (
    execute_all,
    execute_first,
    update_entity,
)


def item_save_serv(
    db: Session, file: UploadFile, path: str, ownerid: str, parentid: str | None
) -> Item:
    folders_save, file_save = create_file_structure(
        file, path, ownerid, bucketid="files"
    )

    crr_parentid = parentid

    for f in folders_save:
        folder = execute_first(
            item_by_ownerid_parentid(db, ownerid, crr_parentid, f.path)
        )
        if folder:
            continue
        item = item_save(db, f)
        crr_parentid = item.id

    storage.save("files", file.content_type, file_save.path, file.file)

    item_save(db, file_save)

    return None


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
