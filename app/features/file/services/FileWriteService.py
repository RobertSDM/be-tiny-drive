import copy
import io
from typing import List, Optional, Union
from uuid import uuid4

from PIL import Image
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.exceptions import (
    DomainError,
    FileValidationError,
    InvalidFileName,
)
from app.lib.supabase.storage import supabase_storage_client
from app.lib.sqlalchemy import client
from app.database.models.FileModel import FileModel
from app.database.repositories.file_repo import (
    file_by_ownerid_parentid_fullname,
    file_save,
)
from app.features.file.utils import (
    file_exists_or_raise,
    verify_name_duplicated,
)
from app.utils.utils import (
    image_to_jpg,
    make_file_bucket_path,
    byte_formatting,
    resize_image,
)
from app.core.constants import MAX_FILESIZE, MAX_RECURSIVE_DEPTH, SUPA_BUCKETID
from app.utils.utils import validate_filename


class FileWriteService:

    def __init__(self):
        self.MAX_RETRY = 3

    def _create_file_and_folders(
        self, metadata: UploadFile, ownerid: str
    ) -> tuple[FileModel, List[FileModel]]:
        folders: List[FileModel] = list()

        dirs = metadata.filename.split("/")
        folder_names = dirs[:-1]

        for name in folder_names:
            folder = FileModel(
                extension="",
                parentid=None,
                size=0,
                size_prefix="",
                content_type="",
                filename=name,
                ownerid=ownerid,
                is_dir=True,
            )
            folders.append(folder)

        name_splited = dirs[-1].split(".")
        name = ".".join(name_splited[:-1])
        extension = f".{name_splited[-1]}" if len(name_splited) > 1 else ""
        size, prefix = byte_formatting(metadata.size)

        file = FileModel(
            id=str(uuid4()),
            filename=name,
            extension=extension,
            parentid=None,
            content_type=metadata.content_type,
            size=size,
            size_prefix=prefix,
            ownerid=ownerid,
        )

        return file, folders

    def _find_first_ancestor_in_common(
        self,
        db: Session,
        ownerid: str,
        start_parentid: str | None,
        folders: List[FileModel],
    ):
        """
        Finds the first ancestor in common between the files you want to save and the paths in the database.

        Returns:
         -1 as index if all the files are in the database
        """

        parentid = copy.copy(start_parentid)

        for i, f in enumerate(folders):
            folder = file_by_ownerid_parentid_fullname(
                db, ownerid, parentid, f.filename, True
            ).first()

            if not folder:
                return parentid, i

            parentid = folder.id

        return parentid, -1

    def _save_folders(
        self, db: Session, parentid: str | None, folders: list[FileModel]
    ) -> tuple[FileModel, str]:
        """
        Create de necessary folders to fill the file path
        """

        curr_parentid = parentid

        for f in folders:
            f.parentid = curr_parentid
            file_save(db, f)
            curr_parentid = f.id

        return curr_parentid

    def save_file(
        self,
        db: Session,
        metadata: List[UploadFile],
        ownerid: str,
        parentid: Union[str, None],
    ) -> FileModel:
        files: List[FileModel] = list()

        try:
            for meta in metadata:
                # Extracting metadata
                name = meta.filename.split("/")[-1].split(".")[0]

                if meta.size > MAX_FILESIZE:
                    raise DomainError(
                        f'The file "{name}" is to large. The maximum file size is {MAX_FILESIZE / 1024**2:.0f}Mbs',
                        422,
                    )

                if not validate_filename(name):
                    raise InvalidFileName(name)

                if parentid is not None:
                    file_exists_or_raise(db, ownerid, parentid)

                file, folders = self._create_file_and_folders(
                    meta,
                    ownerid,
                )

                # TODO: find other way to treat max depth
                if len(folders) > MAX_RECURSIVE_DEPTH:
                    raise FileValidationError(
                        f"The item '{file.filename + file.extension}' exceeds the maximum depth {MAX_RECURSIVE_DEPTH}"
                    )

                start_parentid, folders_start_index = (
                    self._find_first_ancestor_in_common(db, ownerid, parentid, folders)
                )

                verify_name_duplicated(
                    db, ownerid, start_parentid, meta.filename, False
                )

                # If all the folders don't form a path
                if folders_start_index != -1:
                    for f in folders:
                        f.parentid = start_parentid
                        file_save(db, f)

                        if f.parentid == parentid:
                            files.append(f)

                        start_parentid = f.id

                file.parentid = start_parentid
                file_save(db, file)
                files.append(file)

                supabase_storage_client.save(
                    SUPA_BUCKETID,
                    meta.content_type,
                    make_file_bucket_path(ownerid, file.id, "file"),
                    io.BufferedReader(meta.file),
                )
        except Exception as e:
            for file in files:
                if file.is_dir:
                    continue

                supabase_storage_client.remove(
                    SUPA_BUCKETID,
                    make_file_bucket_path(ownerid, file.id, "file"),
                )

            raise e

        return files

    def save_folder(
        self, db: Session, ownerid: str, parentid: Optional[str], name: str
    ) -> FileModel:
        if not validate_filename(name):
            raise InvalidFileName(name)

        if parentid is not None:
            file_exists_or_raise(db, ownerid, parentid)

        verify_name_duplicated(db, ownerid, parentid, name, True)

        folder = FileModel(
            filename=name,
            ownerid=ownerid,
            parentid=parentid,
            content_type="",
            extension="",
            size=0,
            size_prefix="",
            is_dir=True,
        )

        file_save(db, folder)

        return folder

    def create_preview(self, ownerid: str, files: List[FileModel]):
        session = next(client.get_session())

        for file in files:
            session.add(file)

            if not file.content_type.startswith("image"):
                return

            bytedata = supabase_storage_client.download(
                SUPA_BUCKETID, make_file_bucket_path(ownerid, file.id, "file")
            )

            image = Image.open(io.BytesIO(bytedata))
            image = resize_image(image)
            image = image_to_jpg(image)

            supabase_storage_client.save(
                SUPA_BUCKETID,
                "image/jpg",
                make_file_bucket_path(ownerid, file.id, "preview"),
                io.BufferedReader(image),
            )
