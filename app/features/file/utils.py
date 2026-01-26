import io
import os
from typing import BinaryIO, Generator, List, Literal, Optional
import zipfile
from sqlalchemy.orm import Session, InstrumentedAttribute
from sqlalchemy import UnaryExpression
import storage3

from app.core.constants import SUPA_BUCKETID
from app.core.exceptions import (
    FileAlreadyExists,
    FileNotFound,
    FolderNotFound,
)
from app.core.schemas import SortColumn, SortOrder
from app.database.models.FileModel import FileModel
from app.database.repositories.file_repo import (
    file_by_id_ownerid,
    file_by_ownerid_parentid,
    file_by_id_ownerid_is_dir,
    file_by_ownerid_parentid_fullname,
)
from app.lib.supabase.storage import supabase_storage_client
from app.utils.utils import make_file_bucket_path


def get_files(db: Session, ownerid: str, fileids: list[str]) -> list[FileModel]:
    """
    Get all [File] models from a list of ids
    """

    files = list()

    for id in fileids:
        file = get_file_or_raise(
            db,
            ownerid,
            id,
        )
        files.append(file)

    return files


def get_file_or_raise(
    db: Session, ownerid: str, id_: str, is_dir: Optional[bool] = None
) -> FileModel:
    """
    Get the file from the database, if it doesn't exist raise [NotFound] error
    """

    file: Optional[FileModel] = None

    if is_dir is None:
        file = file_by_id_ownerid(db, id_, ownerid).first()
    else:
        file = file_by_id_ownerid_is_dir(db, id_, ownerid, is_dir).first()

    if not file:
        if is_dir:
            raise FolderNotFound()
        else:
            raise FileNotFound()

    return file


def zip_files(files: List[FileModel], ownerid: str, path: str) -> io.BytesIO:
    """
    Create a zip file within a [io.BytesIO] with all files requested
    """

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zip_:
        for file in files:
            bytedata = supabase_storage_client.download(
                SUPA_BUCKETID, make_file_bucket_path(ownerid, file.id, "file")
            )

            file_path = os.path.join(path, f"{file.filename}{file.extension}")

            zip_.writestr(file_path, bytedata)

    buf.seek(0)
    return buf


def file_exists_or_raise(
    db: Session, ownerid: str, id_: str, is_dir: Optional[bool] = None
):
    exists = False

    if is_dir is not None:
        exists = db.query(
            file_by_id_ownerid_is_dir(db, id_, ownerid, is_dir).exists()
        ).scalar()
    else:
        exists = db.query(file_by_id_ownerid(db, id_, ownerid).exists()).scalar()

    if not exists:
        if not is_dir:
            raise FileNotFound()
        else:
            raise FolderNotFound()


def zip_folder(db: Session, ownerid: str, root: FileModel) -> io.BytesIO:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zip_:

        def dfs(path: str, parentid: str):
            files = file_by_ownerid_parentid(db, ownerid, parentid).all()
            if len(files) == 0:
                # Just returning, not adding folders with no content
                return

            for file in files:
                if file.is_dir:
                    dfs(os.path.join(path, file.filename), file.id)
                else:
                    bytedata = supabase_storage_client.download(
                        SUPA_BUCKETID, make_file_bucket_path(ownerid, file.id, "file")
                    )
                    file_path = os.path.join(path, f"{file.filename}{file.extension}")
                    zip_.writestr(file_path, bytedata)

        dfs("", root.id)

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


def column_from_sort(type_: SortColumn) -> InstrumentedAttribute:
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
        raise FolderNotFound()

    return folder


def verify_name_duplicated(
    db: Session,
    ownerid: str,
    parentid: str | None,
    filename: str,
    is_dir: bool,
) -> None:
    """
    Raise [FileAlreadyExists]
    """

    fullname = filename.split("/")[-1]
    exists = db.query(
        file_by_ownerid_parentid_fullname(
            db, ownerid, parentid, fullname, is_dir
        ).exists()
    ).scalar()

    if exists:
        raise FileAlreadyExists(fullname, "file")


def delete_file_from_storage(fileid: str, previewid: Optional[str] = None):
    try:
        supabase_storage_client.remove(
            SUPA_BUCKETID,
            fileid,
        )

        if previewid is not None:
            supabase_storage_client.remove(
                SUPA_BUCKETID,
                previewid,
            )
    except storage3.exceptions.StorageApiError as e:
        if e.code == "NoSuchUpload":
            raise FileNotFound()
