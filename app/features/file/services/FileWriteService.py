import io
from tabnanny import filename_only
from typing import List, Optional, Union
from uuid import uuid4

from PIL import Image
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.validation_errors import InvalidFileName, ItemToDeep
from app.lib.supabase.storage import (
    supabase_storage_client as storage_client,
)
from app.lib.sqlalchemy import client
from app.core.exceptions import (
    ParentNotFound,
)
from app.database.models.FileModel import FileModel
from app.database.repositories.item_repo import (
    file_by_id_ownerid,
    file_by_ownerid_parentid_fullname_alive,
    item_save,
)
from app.core.schemas import FileType
from app.features.file.utils import (
    verify_name_duplicated,
    get_file_parent_or_raise,
    upload_file_to_storage,
)
from app.utils.utils import (
    image_to_jpg,
    make_file_bucket_path,
    byte_formatting,
    resize_image,
)
from app.core.constants import MAX_RECURSIVE_DEPTH, SUPA_BUCKETID
from app.utils.utils import validate_filename


class FileWriteService:

    def __init__(self):
        self.MAX_RETRY = 3

    def _create_file(
        self, metadata: UploadFile, ownerid: str
    ) -> tuple[List[FileModel], FileModel]:
        folders: List[FileModel] = list()

        dirs = metadata.filename.split("/")
        folder_names = dirs[:-1]

        for i, name in enumerate(folder_names):
            folder = FileModel(
                extension="",
                parentid=None,
                size=0,
                size_prefix="",
                content_type="",
                filename=name,
                ownerid=ownerid,
                type=FileType.FOLDER,
            )
            folders.append(folder)

        name_splited = dirs[-1].split(".")
        extension = name_splited[-1] if len(name_splited) > 1 else ""
        size, prefix = byte_formatting(metadata.size)

        file = FileModel(
            id=str(uuid4()),
            filename=name_splited[0],
            extension=extension,
            parentid=None,
            content_type=metadata.content_type,
            size=size,
            size_prefix=prefix,
            ownerid=ownerid,
            type=FileType.FILE,
        )

        return file, folders

    def _find_path_intersection(
        self, db: Session, ownerid: str, parentid: str | None, folders: List[FileModel]
    ):
        """
        Finds where the path provided start is located in the FHT
        """

        crr_parentid = parentid

        for i, f in enumerate(folders):
            folder = file_by_ownerid_parentid_fullname_alive(
                db, ownerid, crr_parentid, f.filename, f.type
            ).first()

            if not folder:
                return crr_parentid, i

            crr_parentid = folder.id

        return crr_parentid, -1

    def _create_folders(
        self, db: Session, parentid: str | None, folders: list[FileModel]
    ) -> tuple[FileModel, str]:
        """
        Create de necessary folders to fill the file path
        """

        curr_parentid = parentid
        first_folder = None

        for f in folders:
            f.parentid = curr_parentid
            item_save(db, f)
            curr_parentid = f.id

            if not first_folder:
                first_folder = f

        return first_folder, curr_parentid

    def save_file(
        self,
        db: Session,
        metadata: UploadFile,
        ownerid: str,
        parentid: Union[str, None],
    ) -> FileModel:
        name = metadata.filename.split("/")[-1].split(".")[0]

        if not validate_filename(name):
            raise InvalidFileName(name)

        if parentid is not None:
            exists = db.query(
                file_by_id_ownerid(db, parentid, ownerid).exists()
            ).scalar()

            if not exists:
                raise ParentNotFound()

        file, folders = self._create_file(
            metadata,
            ownerid,
        )

        # TODO: find other way to treat max depth
        if len(folders) > MAX_RECURSIVE_DEPTH:
            raise ItemToDeep(file.filename + file.extension)

        curr_parentid, folder_start_id = self._find_path_intersection(
            db, ownerid, parentid, folders
        )

        verify_name_duplicated(
            db, ownerid, curr_parentid, metadata.filename, FileType.FILE
        )

        if folder_start_id != -1:
            first_folder, curr_parentid = self._create_folders(
                db, curr_parentid, folders[folder_start_id:]
            )

        file.parentid = curr_parentid
        item_save(db, file)

        upload_file_to_storage(
            metadata.file.read(),
            metadata.content_type,
            make_file_bucket_path(ownerid, file.id, "file"),
        )

        return file if len(folders) == 0 else first_folder

    def save_folder(
        self, db: Session, ownerid: str, parentid: Optional[str], name: str
    ) -> FileModel:
        if not validate_filename(name):
            raise InvalidFileName(name)

        if parentid is not None:
            exists = db.query(
                file_by_id_ownerid(db, parentid, ownerid).exists()
            ).scalar()

            if not exists:
                raise ParentNotFound()

        verify_name_duplicated(db, ownerid, parentid, name, FileType.FOLDER)

        folder = FileModel(
            filename=name,
            ownerid=ownerid,
            parentid=parentid,
            content_type="",
            extension="",
            size=0,
            size_prefix="",
            type=FileType.FOLDER,
        )

        item_save(db, folder)

        return folder

    def create_preview(self, ownerid: str, file: FileModel):
        session = next(client.get_session())

        session.add(file)

        if not file.content_type.startswith("image"):
            return

        bytedata = storage_client.download(
            SUPA_BUCKETID, make_file_bucket_path(ownerid, file.id, "file")
        )

        image = Image.open(io.BytesIO(bytedata))
        image = resize_image(image)
        image = image_to_jpg(image)

        upload_file_to_storage(
            image.read(),
            "image/jpg",
            make_file_bucket_path(ownerid, file.id, "preview"),
        )
