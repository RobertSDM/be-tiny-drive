from uuid import uuid4
from fastapi import UploadFile
import storage3
from sqlalchemy.orm import Session

from app.features.auth.client.supabase.storage_client import storage
from app.core.exceptions import ItemExistsInFolder
from app.database.models.item_model import Item
from app.database.repositories.item_repo import (
    item_by_ownerid_parentid_fullname,
    item_save,
)
from app.enums.enums import ItemType
from app.interfaces.storage_interface import StorageClientInterface
from app.features.items.services import item_checks
from app.utils.query import exec_first
from app.utils.utils import make_bucket_path, normalize_file_size
from app.constants.env import drive_bucketid


class _ItemCreateServ:

    def _create_items_from_path(
        self, file_data: UploadFile, ownerid: str
    ) -> tuple[list[Item], Item]:
        folders = list()

        dirs: list[str] = file_data.filename.split("/")
        folder_names: list[str] = dirs[:-1]

        for name in folder_names:
            folder = Item(
                id=str(uuid4()),
                extension="",
                parentid=None,
                size=0,
                size_prefix="",
                content_type="",
                name=name,
                ownerid=ownerid,
                type=ItemType.FOLDER,
            )
            folders.append(folder)

        name_splited = dirs[-1].split(".")
        name = ".".join(name_splited[:-1]) if len(name_splited) > 1 else name_splited[0]
        extension = (
            f".{name_splited[-1]}"
            if len(name_splited) > 1 and name_splited[-1] != ""
            else ""
        )
        normalized_size, prefix = normalize_file_size(file_data.size)

        file = Item(
            id=str(uuid4()),
            name=name,
            extension=extension,
            parentid=None,
            content_type=file_data.content_type,
            size=normalized_size,
            size_prefix=prefix,
            ownerid=ownerid,
            type=ItemType.FILE,
        )

        return folders, file

    def _upload_file_to_storage(
        self, filedata: UploadFile, file: Item, storage: StorageClientInterface
    ):
        try:
            storage.save(
                drive_bucketid,
                filedata.content_type,
                make_bucket_path(file),
                filedata.file.read(),
            )
        except storage3.exceptions.StorageApiError as e:
            if e.status == "409":
                raise ItemExistsInFolder(file.name, file.type.value)

            raise e

    def _create_folders(
        self, db: Session, ownerid: str, parentid: str | None, folders: list[Item]
    ) -> str | None:
        crr_parentid = parentid

        for f in folders:
            folder = exec_first(
                item_by_ownerid_parentid_fullname(db, ownerid, crr_parentid, f.name)
            )

            if folder:
                crr_parentid = folder.id
                continue

            f.parentid = crr_parentid
            crr_parentid = f.id
            item_save(db, f)

        return crr_parentid

    def item_save_item_serv(
        self, db: Session, filedata: UploadFile, ownerid: str, parentid: str | None
    ) -> Item:

        item_checks.check_parent_exists(db, ownerid, parentid)

        folders, file = self._create_items_from_path(
            filedata,
            ownerid,
        )

        self._upload_file_to_storage(filedata, file, storage)
        crr_parentid = self._create_folders(db, ownerid, parentid, folders)

        item_checks.check_duplicate_name(
            db, ownerid, crr_parentid, filedata.filename, ItemType.FILE.value
        )

        file.parentid = crr_parentid
        return item_save(db, file)

    def item_save_folder_serv(
        self, db: Session, ownerid: str, name: str, parentid: str | None
    ):
        item_checks.check_duplicate_name(
            db, ownerid, parentid, name, ItemType.FOLDER.value
        )
        item_checks.check_parent_exists(db, ownerid, parentid)

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


item_create_serv = _ItemCreateServ()
