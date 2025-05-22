import io
from typing import Optional
import zipfile
from fastapi import UploadFile
from sqlalchemy import except_all
from sqlalchemy.orm import Session
import storage3
import storage3.exceptions

from app.clients.supabase.storage_client import storage
from app.core.exceptions import (
    InvalidItemToPreview,
    ItemExistsInFolder,
    ItemNotFound,
    ParentFolderNotFound,
)
from app.core.extract_file_metadata import create_items_from_path
from app.database.models import Item
from app.database.repositories.item_repo import (
    item_by_id_ownerid,
    item_by_ownerid_parentid,
    item_by_ownerid_parentid_fullname,
    item_delete,
    item_save,
    items_by_ownerid_name,
    items_by_ownerid_name_type,
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
    db: Session, file_data: UploadFile, ownerid: str, parentid: str | None
) -> Item:
    item = execute_first(
        item_by_ownerid_parentid_fullname(
            db, ownerid, parentid, f"{file_data.filename.split("/")[-1]}"
        )
    )
    if item:
        raise ItemExistsInFolder(file_data.filename.split("/")[-1], ItemType.FILE.value)

    if parentid:
        parent_exists = execute_exists(db, item_by_id_ownerid(db, parentid, ownerid))
        if not parent_exists:
            raise ParentFolderNotFound()

    folders, file = create_items_from_path(
        file_data,
        ownerid,
    )

    try:
        storage.save(
            drive_bucketid,
            file_data.content_type,
            make_bucket_path(file),
            file_data.file.read(),
        )
    except storage3.exceptions.StorageApiError as e:
        if e.status == "409":
            raise ItemExistsInFolder(file.name, file.type.value)

        raise e

    crr_parentid = parentid

    for f in folders:
        folder = execute_first(
            item_by_ownerid_parentid_fullname(db, ownerid, crr_parentid, f.name)
        )

        if folder:
            crr_parentid = folder.id
            continue

        f.parentid = crr_parentid
        crr_parentid = f.id
        item_save(db, f)

    file.parentid = crr_parentid
    return item_save(db, file)


def item_save_folder_serv(db: Session, ownerid: str, name: str, parentid: str | None):
    if parentid:
        parent = execute_exists(db, item_by_id_ownerid(db, parentid, ownerid))
        if not parent:
            raise ParentFolderNotFound()

    item = execute_first(item_by_ownerid_parentid_fullname(db, ownerid, parentid, name))

    if item:
        raise ItemExistsInFolder(name, ItemType.FOLDER.value)

    folder = Item(
        name=name,
        ownerid=ownerid,
        parentid=parentid,
        content_type="",
        extension="",
        size=0,
        size_prefix="",
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
        raise ItemNotFound()

    return item


def all_items_in_folder_serv(db: Session, ownerid: str, parentid: Optional[str]):
    return execute_all(item_by_ownerid_parentid(db, ownerid, parentid))


def delete_item_serv(db: Session, ownerid: str, id: str) -> Item:
    item = execute_first(item_by_id_ownerid(db, id, ownerid))

    if not item:
        raise ItemNotFound()

    if item.type == ItemType.FOLDER:
        items = execute_all(item_by_ownerid_parentid(db, ownerid, item.id))

        def dfs(children: list[Item]):
            for c in children:
                bucket_item_path = make_bucket_path(c)
                if c.type == ItemType.FOLDER:
                    children = execute_all(item_by_ownerid_parentid(db, ownerid, c.id))
                    dfs(children)
                else:
                    storage.remove(drive_bucketid, bucket_item_path)

        dfs(items)
    else:
        storage.remove(
            drive_bucketid,
            make_bucket_path(item),
        )

    item_delete(db, item)

    return item


def download_serv(db, id: str, ownerid: str) -> str:
    item = execute_first(item_by_id_ownerid(db, id, ownerid))

    if not item:
        raise ItemNotFound()

    if item.type == ItemType.FILE:
        bucket_item_path = make_bucket_path(item)
        url = storage.signedURL(
            drive_bucketid, bucket_item_path, 5 * 60, f"{item.name}{item.extension}"
        )

        return url

    return ""


def download_many_serv(db: Session, fileids: list[str], ownerid: str):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip:
        for id in fileids:
            item = execute_first(item_by_id_ownerid(db, id, ownerid))
            if not item:
                raise ItemNotFound()

            try:
                file = storage.download(
                    drive_bucketid,
                    make_bucket_path(item),
                )

                zip.writestr(f"{item.name}{item.extension}", file)

            except Exception as e:
                raise e

    buffer.seek(0)
    while 1:
        b = buffer.read(5 * (1024 * 1024))  # 5mbs
        if len(b) == 0:
            break
        yield b


def download_folder_serv(db: Session, ownerid: str, parentid: str):
    folder = execute_first(item_by_id_ownerid(db, parentid, ownerid))

    if not folder:
        raise ParentFolderNotFound()

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip:

        def dfs(folder: Item, path: str):
            items = execute_all(item_by_ownerid_parentid(db, ownerid, folder.id))

            for item in items:
                if item.type == ItemType.FILE:
                    try:
                        file = storage.download(
                            drive_bucketid,
                            make_bucket_path(item),
                        )

                        file_path = (
                            f"{path}/" if len(path) > 0 else ""
                        ) + f"{item.name}{item.extension}"
                        zip.writestr(
                            file_path,
                            file,
                        )

                    except Exception as e:
                        raise e
                else:

                    folder_path = (f"{path}/" if len(path) > 0 else "") + f"{item.name}"

                    dfs(item, folder_path)

        dfs(folder, "")

    buffer.seek(0)
    while 1:
        b = buffer.read(5 * 1024 * 1024)
        if len(b) == 0:
            break
        yield b


def image_preview_serv(db: Session, ownerid: str, id: str) -> str:
    item = execute_first(item_by_id_ownerid(db, id, ownerid))

    if not item:
        raise ItemNotFound()

    if not item.content_type.startswith("image"):
        raise InvalidItemToPreview()

    try:
        bucket_item_path = make_bucket_path(item)
        url = storage.signedURL(drive_bucketid, bucket_item_path, 3600)
    except Exception as e:
        raise e
    return url


def search_serv(
    db: Session, ownerid: str, query: str, type: ItemType | None
) -> list[Item]:
    if type:
        items = execute_all(items_by_ownerid_name_type(db, ownerid, query, type))
    else:
        items = execute_all(items_by_ownerid_name(db, ownerid, query))
    return items
