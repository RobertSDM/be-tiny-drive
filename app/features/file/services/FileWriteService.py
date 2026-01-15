import io
from typing import List, Union
from uuid import uuid4

from PIL import Image
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.validation_errors import InvalidFileName, ItemToDeep
from app.lib.supabase.storage import (
    supabase_storage_client as storage_client,
)
from app.core.exceptions import (
    NotSupported,
    NotFound,
    ParentNotFound,
)
from app.database.models.FileModel import FileModel
from app.database.repositories.item_repo import (
    file_by_id_ownerid,
    file_by_ownerid_parentid_fullname_alive,
    item_save,
)
from app.core.schemas import FileType
from app.utils.query import exec_first
from app.features.file.utils import (
    verify_name_duplicated,
    get_file_parent_or_raise,
    upload_file_to_storage,
)
from app.utils.utils import (
    image_to_jpg,
    make_file_bucket_path,
    byte_formatting,
    pipeline,
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
                db, ownerid, crr_parentid, f.filename
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
            saved_folder = item_save(db, f)
            curr_parentid = saved_folder.id

            if not first_folder:
                first_folder = saved_folder

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
        saved_item = item_save(db, file)

        upload_file_to_storage(
            metadata.file.read(),
            metadata.content_type,
            make_file_bucket_path(ownerid, saved_item.id, "file"),
            file,
        )

        return saved_item if len(folders) == 0 else first_folder

    def save_folder(self, db: Session, ownerid: str, name: str, parentid: str | None):
        if not validate_filename(name):
            raise InvalidFileName(name)

        verify_name_duplicated(db, ownerid, parentid, name, FileType.FOLDER)
        get_file_parent_or_raise(db, ownerid, parentid)

        folder = FileModel(
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

    # def create_preview(self, db: Session, ownerid: str, id: str):
    #     item = exec_first(file_by_id_ownerid(db, id, ownerid))
    #     if not item:
    #         raise NotFound()

    #     if item.content_type.startswith("image"):
    #         bytedata = storage_client.download(
    #             SUPA_BUCKETID, make_file_bucket_path(item)
    #         )

    #         data = pipeline(
    #             lambda b: Image.open(io.BytesIO(b)),
    #             resize_image,
    #             image_to_jpg,
    #         )(bytedata)

    #         upload_file_to_storage(
    #             data.read(),
    #             "image/jpg",
    #             make_file_preview_bucket_path(item),
    #             item,
    #         )
    #         db.commit()
    #     else:
    #         db.commit()
    #         raise NotSupported()
