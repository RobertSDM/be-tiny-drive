import io
from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
import storage3
import storage3.exceptions

from app.clients.supabase_storage_client import storage
from app.core.exceptions import (
    ItemExistsInFolder,
    ItemNotFound,
    AccountDoesNotExists,
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
from app.database.repositories.account_repo import account_by_id
from app.database.repositories.item_repo import item_by_ownerid_parentid_path
from app.utils.execute_query import (
    execute_all,
    execute_exists,
    execute_first,
    update_entity,
)


def item_save_serv(
    db: Session, file: UploadFile, path: str, ownerid: str, parentid: str | None
) -> Item:
    exists = execute_exists(db, account_by_id(db, ownerid))

    if not exists:
        raise AccountDoesNotExists()

    bucketid = "files"

    folders_save, file_save = create_file_structure(file, path, ownerid, bucketid)

    crr_parentid = parentid

    try:
        storage.save(bucketid, file.content_type, file_save.path, file.file.read())
    except storage3.exceptions.StorageApiError as e:
        if e.status == "409":
            raise ItemExistsInFolder(file_save.name, file_save.type.value)

        raise e

    for f in folders_save:
        folder = execute_first(
            item_by_ownerid_parentid_path(db, crr_parentid, ownerid, f.path)
        )
        if folder:
            crr_parentid = folder.id
            continue
        item = item_save(db, f)
        crr_parentid = item.id

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
