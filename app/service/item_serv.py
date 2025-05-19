from typing import Optional
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
import storage3
import storage3.exceptions

from app.clients.supabase.storage_client import storage
from app.core.exceptions import (
    ItemExistsInFolder,
    ItemNotFound,
    AccountDoesNotExists,
    ParentFolderNotFound,
)
from app.core.extract_file_metadata import create_items_from_path
from app.database.models import Item
from app.database.repositories import (
    item_save,
    item_by_ownerid_parentid,
    item_by_id_ownerid,
    item_delete,
)
from app.database.repositories.account_repo import account_by_id
from app.database.repositories.item_repo import (
    item_by_ownerid_path,
)
from app.constants.env_ import drive_bucketid
from app.enums.enums import ItemType
from app.utils.execute_query import (
    execute_all,
    execute_exists,
    execute_first,
    update_entity,
)
from app.utils.utils import make_bucket_path


def item_save_item_serv(
    db: Session, file: UploadFile, ownerid: str, parentid: str | None
) -> Item:
    account_exists = execute_exists(db, account_by_id(db, ownerid))

    if not account_exists:
        raise AccountDoesNotExists()

    parent_path = ""
    if parentid:
        parent = execute_first(item_by_id_ownerid(db, parentid, ownerid))
        if not parent:
            raise ParentFolderNotFound()
        parent_path = parent.path

    bucket_file_hash = str(uuid4())
    item_folders, item_file = create_items_from_path(
        file, ownerid, bucket_file_hash, parent_path
    )

    try:
        storage.save(
            drive_bucketid,
            file.content_type,
            make_bucket_path(
                ownerid, item_file.path, f"{bucket_file_hash}.{item_file.extension}"
            ),
            file.file.read(),
        )
    except storage3.exceptions.StorageApiError as e:
        if e.status == "409":
            raise ItemExistsInFolder(item_file.name, item_file.type.value)

        raise e

    crr_parentid = parentid
    if len(item_folders) > 0 and (
        folder := execute_first(
            item_by_ownerid_path(db, ownerid, item_folders[-1].path)
        )
    ):
        crr_parentid = folder.id
    else:
        for f in item_folders:
            if folder := execute_first(item_by_ownerid_path(db, ownerid, f.path)):
                crr_parentid = folder.id
                continue
            f.parentid = crr_parentid
            item = item_save(db, f)
            crr_parentid = item.id

    item_file.parentid = crr_parentid
    return item_save(db, item_file)


def item_save_folder_serv(db: Session, ownerid: str, name: str, parentid: str | None):
    account_exists = execute_exists(db, account_by_id(db, ownerid))

    if not account_exists:
        raise AccountDoesNotExists()

    parent_path = ""
    if parentid:
        parent = execute_first(item_by_id_ownerid(db, parentid, ownerid))
        if not parent:
            raise ParentFolderNotFound()
        parent_path = parent.path

    folder = Item(
        name=name,
        ownerid=ownerid,
        parentid=parentid,
        extension="",
        size=0,
        size_prefix="",
        bucketid=None,
        path=f"{parent_path}/{name}" if parent_path != "" else name,
        type=ItemType.FOLDER,
    )

    return item_save(db, folder)


def item_update_name(db: Session, id: str, ownerid: str, name: str) -> Item:
    query = item_by_id_ownerid(db, id, ownerid)
    item = execute_first(query)
    if not item:
        raise ItemNotFound()

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

    bucket_path = f"user-{ownerid}/drive"

    if item.type == ItemType.FOLDER:
        storage_list = storage.list(drive_bucketid, f"{bucket_path}/{item.path}")

        def dfs(to_visit: list[str], path: str = ""):
            for tv in to_visit:
                bucket_item_path = make_bucket_path(ownerid, item.path, tv["name"])
                if not tv["metadata"]:
                    children = storage.list(drive_bucketid, bucket_item_path)
                    dfs(children, f"{path}/{tv["name"]}")
                else:
                    storage.remove(drive_bucketid, bucket_item_path)

        dfs(storage_list, item.path)
    else:
        bucket_fullname = f"{item.bucketid}.{item.extension}"
        storage.remove(
            drive_bucketid,
            make_bucket_path(ownerid, item.path, bucket_fullname),
        )

    item_delete(db, item)

    return item


def download_serv(db, id: str, ownerid: str) -> str:
    account_exists = execute_exists(db, account_by_id(db, ownerid))

    if not account_exists:
        raise AccountDoesNotExists()

    item = execute_first(item_by_id_ownerid(db, id, ownerid))

    if not item:
        raise ItemNotFound()

    if item.type == ItemType.FILE:
        bucket_fullname = f"{item.name}.{item.extension}"
        bucket_item_path = make_bucket_path(ownerid, item.path, bucket_fullname)
        url = storage.signedURL(
            drive_bucketid, bucket_item_path, 5 * 60, bucket_fullname
        )

        return url

    return ""
