import io
from uuid import uuid4

from PIL import Image
from fastapi import UploadFile
import storage3
from sqlalchemy.orm import Session
import storage3.exceptions

from app.core.validation_errors import InvalidItemName, ItemToDeep
from app.features.storage.supabase_storage_client import (
    supabase_storage_client as storage_client,
)
from app.core.exceptions import (
    FeatureNotSupported,
    ItemExistsInFolder,
    ItemKeyExistsInStorage,
    ItemNotFound,
)
from app.database.models.item_model import Item
from app.database.repositories.item_repo import (
    item_by_id_ownerid,
    item_by_ownerid_parentid_fullname,
    item_by_ownerid_parentid_fullname_non_deleted,
    item_save,
)
from app.enums.enums import ItemType, ProcessingState
from app.features.items.services.item_checks import item_checks
from app.utils.query import exec_first, update
from app.utils.utils import (
    compress_file,
    decompress,
    image_to_jpg,
    make_bucket_file_path,
    make_bucket_file_preview_path,
    normalize_file_size,
    pipeline,
    resize_image,
)
from app.constants.env import drive_bucketid
from app.core.validations import validate_item_name, max_folder_depth


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
                processing_state=ProcessingState.COMPLETE.value,
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
        self, filedata: bytes, content_type: str, path: str, file: Item
    ):
        try:
            storage_client.save(drive_bucketid, content_type, path, filedata)
        except storage3.exceptions.StorageApiError as e:
            match e.code:
                case "ResourceAlreadyExists":
                    raise ItemExistsInFolder(file.name, file.type.value)
                case "KeyAlreadyExists":
                    raise ItemKeyExistsInStorage()

            raise e

    def _create_folders(
        self, db: Session, ownerid: str, parentid: str | None, folders: list[Item]
    ) -> tuple[Item, str]:
        crr_parentid = parentid
        first_folder = None

        for f in folders:
            folder = exec_first(
                item_by_ownerid_parentid_fullname_non_deleted(db, ownerid, crr_parentid, f.name)
            )

            if folder:
                crr_parentid = folder.id
                continue

            f.parentid = crr_parentid
            crr_parentid = f.id
            
            saved_folder = item_save(db, f)

            if not first_folder:
                first_folder = saved_folder

        return first_folder, crr_parentid

    def item_save_item_serv(
        self, db: Session, filedata: UploadFile, ownerid: str, parentid: str | None
    ) -> Item:
        name = filedata.filename.split("/")[-1].split(".")[0]

        if not validate_item_name(name):
            raise InvalidItemName(name)

        item_checks.check_parent_exists(db, ownerid, parentid)

        max_retries, retries = 3, 0

        while retries < max_retries:
            folders, file = self._create_items_from_path(
                filedata,
                ownerid,
            )

            if len(folders) > max_folder_depth:
                raise ItemToDeep(file.name + file.extension)

            data = pipeline(
                compress_file,
            )(filedata.file.read())

            try:
                self._upload_file_to_storage(
                    data, filedata.content_type, make_bucket_file_path(file), file
                )
                break
            except ItemKeyExistsInStorage as e:
                retries += 1
                if retries == max_retries:
                    raise e

        first_folder, crr_parentid = self._create_folders(
            db, ownerid, parentid, folders
        )

        item_checks.check_duplicate_name(
            db, ownerid, crr_parentid, filedata.filename, ItemType.FILE
        )

        file.parentid = crr_parentid
        saved_item = item_save(db, file)

        print(first_folder)
        return saved_item if len(folders) == 0 else first_folder

    def item_save_folder_serv(
        self, db: Session, ownerid: str, name: str, parentid: str | None
    ):
        if not validate_item_name(name):
            raise InvalidItemName(name)

        item_checks.check_duplicate_name(db, ownerid, parentid, name, ItemType.FOLDER)
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

    def item_create_preview_serv(self, db: Session, ownerid: str, id: str):
        item = exec_first(item_by_id_ownerid(db, id, ownerid))
        if not item:
            raise ItemNotFound()

        if item.content_type.startswith("image"):
            bytedata = storage_client.download(
                drive_bucketid, make_bucket_file_path(item)
            )

            data = pipeline(
                decompress,
                lambda b: Image.open(io.BytesIO(b)),
                resize_image,
                image_to_jpg,
            )(bytedata)

            self._upload_file_to_storage(
                data.read(),
                "image/jpg",
                make_bucket_file_preview_path(item),
                item,
            )

            update(
                item_by_id_ownerid(db, id, ownerid),
                {"processing_state": ProcessingState.COMPLETE.value},
            )
            db.commit()
        else:
            update(
                item_by_id_ownerid(db, id, ownerid),
                {"processing_state": ProcessingState.COMPLETE.value},
            )
            db.commit()
            raise FeatureNotSupported()


item_create_serv = _ItemCreateServ()
