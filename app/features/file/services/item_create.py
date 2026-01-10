import io
from uuid import uuid4

from PIL import Image
from fastapi import UploadFile
import storage3
from sqlalchemy.orm import Session
import storage3.exceptions

from app.core.validation_errors import InvalidFileName, ItemToDeep
from app.lib.supabase.storage import (
    supabase_storage_client as storage_client,
)
from app.core.exceptions import (
    NotSupported,
    FileAlreadyExists,
    FileAlreadyExists,
    FileNotFound,
)
from app.database.models.file_model import File
from app.database.repositories.item_repo import (
    item_by_id_ownerid,
    item_by_ownerid_parentid_fullname_non_deleted,
    item_save,
)
from app.core.schemas import FileType
from app.features.file.services.item_checks import item_checks
from app.utils.query import exec_first, update
from app.utils.utils import (
    compress_file,
    decompress,
    image_to_jpg,
    make_bucket_file_path,
    make_bucket_file_preview_path,
    byte_formatting,
    pipeline,
    resize_image,
)
from app.core.constants import MAX_RECURSIVE_DEPTH, SUPA_BUCKETID
from app.utils.utils import validate_item_name


class _ItemCreateServ:

    def _create_items_from_path(
        self, file_data: UploadFile, ownerid: str
    ) -> tuple[list[File], File]:
        folders = list()

        dirs: list[str] = file_data.filename.split("/")
        folder_names: list[str] = dirs[:-1]

        for name in folder_names:
            folder = File(
                id=str(uuid4()),
                extension="",
                parentid=None,
                size=0,
                size_prefix="",
                content_type="",
                name=name,
                ownerid=ownerid,
                type=FileType.FOLDER,
            )
            folders.append(folder)

        name_splited = dirs[-1].split(".")
        name = ".".join(name_splited[:-1]) if len(name_splited) > 1 else name_splited[0]
        extension = (
            f".{name_splited[-1]}"
            if len(name_splited) > 1 and name_splited[-1] != ""
            else ""
        )
        normalized_size, prefix = byte_formatting(file_data.size)

        file = File(
            id=str(uuid4()),
            name=name,
            extension=extension,
            parentid=None,
            content_type=file_data.content_type,
            size=normalized_size,
            size_prefix=prefix,
            ownerid=ownerid,
            type=FileType.FILE,
        )

        return folders, file

    def _upload_file_to_storage(
        self, filedata: bytes, content_type: str, path: str, file: File
    ):
        try:
            storage_client.save(SUPA_BUCKETID, content_type, path, filedata)
        except storage3.exceptions.StorageApiError as e:
            match e.code:
                case "ResourceAlreadyExists":
                    raise FileAlreadyExists(file.filename, file.type.value)
                case "KeyAlreadyExists":
                    raise FileAlreadyExists()

            raise e

    def _create_folders(
        self, db: Session, ownerid: str, parentid: str | None, folders: list[File]
    ) -> tuple[File, str]:
        crr_parentid = parentid
        first_folder = None

        for f in folders:
            folder = exec_first(
                item_by_ownerid_parentid_fullname_non_deleted(
                    db, ownerid, crr_parentid, f.filename
                )
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
    ) -> File:
        name = filedata.filename.split("/")[-1].split(".")[0]

        if not validate_item_name(name):
            raise InvalidFileName(name)

        item_checks.check_parent_exists(db, ownerid, parentid)

        max_retries, retries = 3, 0

        while retries < max_retries:
            folders, file = self._create_items_from_path(
                filedata,
                ownerid,
            )

            if len(folders) > MAX_RECURSIVE_DEPTH:
                raise ItemToDeep(file.filename + file.extension)

            data = pipeline(
                compress_file,
            )(filedata.file.read())

            try:
                self._upload_file_to_storage(
                    data, filedata.content_type, make_bucket_file_path(file), file
                )
                break
            except FileAlreadyExists as e:
                retries += 1
                if retries == max_retries:
                    raise e

        first_folder, crr_parentid = self._create_folders(
            db, ownerid, parentid, folders
        )

        item_checks.check_duplicate_name(
            db, ownerid, crr_parentid, filedata.filename, FileType.FILE
        )

        file.parentid = crr_parentid
        saved_item = item_save(db, file)

        print(first_folder)
        return saved_item if len(folders) == 0 else first_folder

    def item_save_folder_serv(
        self, db: Session, ownerid: str, name: str, parentid: str | None
    ):
        if not validate_item_name(name):
            raise InvalidFileName(name)

        item_checks.check_duplicate_name(db, ownerid, parentid, name, FileType.FOLDER)
        item_checks.check_parent_exists(db, ownerid, parentid)

        folder = File(
            name=name,
            ownerid=ownerid,
            parentid=parentid,
            content_type="",
            extension="",
            size=0,
            size_prefix="",
            type=FileType.FOLDER,
        )

        return item_save(db, folder)

    def item_create_preview_serv(self, db: Session, ownerid: str, id: str):
        item = exec_first(item_by_id_ownerid(db, id, ownerid))
        if not item:
            raise FileNotFound()

        if item.content_type.startswith("image"):
            bytedata = storage_client.download(
                SUPA_BUCKETID, make_bucket_file_path(item)
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
            db.commit()
        else:
            db.commit()
            raise NotSupported()


item_create_serv = _ItemCreateServ()
