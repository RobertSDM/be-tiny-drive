import io
import os
from typing import BinaryIO, Generator, List, Optional
import zipfile
from sqlalchemy.orm import Session, InstrumentedAttribute
from sqlalchemy import UnaryExpression
import storage3

from app.core.constants import SUPA_BUCKETID
from app.core.exceptions import (
    FileAlreadyExists,
    FileNotFound,
    NotFound,
    ParentNotFound,
)
from app.core.schemas import FileType, SortColumn, SortOrder
from app.database.models.FileModel import FileModel
from app.database.repositories.item_repo import (
    file_by_id_ownerid,
    file_by_ownerid_parentid_alive,
    item_by_id_ownerid_type,
    file_by_ownerid_parentid_fullname_alive,
)
from app.lib.supabase.storage import (
    supabase_storage_client as storage_client,
)
from app.utils.utils import make_file_bucket_path


def get_files(db: Session, ownerid: str, fileids: list[str]) -> list[FileModel]:
    """
    Get all [File] models from a list of ids
    """

    files = list()

    for id in fileids:
        file = get_file_or_raise(db, ownerid, id, FileType.FILE)
        files.append(file)

    return files


def get_file_or_raise(
    db: Session, ownerid: str, id: str, type_: Optional[FileType]
) -> FileModel:
    """
    Get the file from the database, if it doesn't exist raise [NotFound] error
    """

    if not type_:
        file = file_by_id_ownerid(db, id, ownerid).first()
    else:
        file = item_by_id_ownerid_type(db, id, ownerid, type_).first()

    if not file:
        raise NotFound(
            f"The {"file" if type_ == FileType.FILE else "folder"} was not found"
        )

    return file


def zip_files(files: List[FileModel], ownerid: str, path: str) -> io.BytesIO:
    """
    Create a zip file within a [io.BytesIO] with all files requested
    """

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zip_:
        for file in files:
            bytedata = storage_client.download(
                SUPA_BUCKETID, make_file_bucket_path(ownerid, file.id, "file")
            )

            file_path = os.path.join(path, f"{file.filename}.{file.extension}")

            zip_.writestr(file_path, bytedata)

    buf.seek(0)
    return buf


def zip_folder(db: Session, ownerid: str, root: FileModel) -> io.BytesIO:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zip_:

        def dfs(path: str):
            files = file_by_ownerid_parentid_alive(db, ownerid, root.id).all()
            if len(files) == 0:
                return

            for file in files:
                if file.type == FileType.FOLDER:
                    dfs(os.path.join(path, file.filename))
                else:
                    bytedata = storage_client.download(
                        SUPA_BUCKETID, make_file_bucket_path(ownerid, file.id, "file")
                    )
                    file_path = os.path.join(path, f"{file.filename}.{file.extension}")
                    zip_.writestr(file_path, bytedata)

        dfs("")

    buf.seek(0)
    return buf


def stream_buffer(buffer: BinaryIO, chunk: int) -> Generator[bytes, None, None]:
    """
    Streams chunks of the data of a buffer
    """

    while True:
        b = buffer.read(chunk)
        if len(b) == 0:
            break
        yield b


def column_and_order_from_file(type_: SortColumn) -> InstrumentedAttribute:
    """
    Return the [File] table column based on the [SortColumn]
    """

    match type_:
        case SortColumn.NAME:
            return FileModel.filename
        case SortColumn.UPDATED_AT:
            return FileModel.updated_at
        case SortColumn.CREATED_AT:
            return FileModel.created_at


def apply_order_to_column(
    order: SortOrder, column: InstrumentedAttribute
) -> UnaryExpression:
    """
    Return the column ordered by the [SortOrder]
    """

    if order == SortOrder.ASC:
        return column.asc()
    else:
        return column.desc()


def get_file_parent_or_raise(db: Session, ownerid: str, parentid: str) -> FileModel:
    folder = file_by_id_ownerid(db, parentid, ownerid).first()

    if not folder:
        raise ParentNotFound()

    return folder


def verify_name_duplicated(
    db: Session,
    ownerid: str,
    parentid: str | None,
    filename: str,
    type_: FileType,
) -> None:
    """
    Raise [FileAlreadyExists]
    """

    fullname = filename.split("/")[-1]
    exists = db.query(
        file_by_ownerid_parentid_fullname_alive(
            db, ownerid, parentid, fullname, type_
        ).exists()
    ).scalar()

    if exists:
        raise FileAlreadyExists(fullname, type_.value)


def upload_file_to_storage(filedata: bytes, content_type: str, path: str):
    storage_client.save(SUPA_BUCKETID, content_type, path, filedata)


def delete_file_from_storage(fileid: str, previewid: str):
    try:
        storage_client.remove(
            SUPA_BUCKETID,
            fileid,
        )

        storage_client.remove(
            SUPA_BUCKETID,
            previewid,
        )
    except storage3.exceptions.StorageApiError as e:
        if e.code == "NoSuchUpload":
            raise FileNotFound()
