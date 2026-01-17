import io
from typing import Any, Generator, List, Optional
from sqlalchemy.orm import Session, Query

from app.core.exceptions import FileBeParent, ParentNotFound
from app.features.file.utils import (
    apply_order_to_column,
    build_zip,
    column_and_order_from_file,
    get_file_or_raise,
    get_files,
    zip_files,
    stream_buffer,
)
from app.lib.supabase.storage import (
    supabase_storage_client as storage_client,
)

from app.database.models import FileModel
from app.database.repositories.item_repo import (
    file_by_ownerid_parentid_alive,
    search_files_by_ownerid_name_type,
)
from app.core.constants import SUPA_BUCKETID
from app.core.schemas import FileType, SortColumn, SortOrder
from app.utils.utils import (
    make_file_bucket_path,
)
from app.core.constants import LIMIT_PER_PAGE, LIMIT_PER_SEARCH


class FileReadService:

    def __init__(self):
        self.STREAM_SIZE = 5 * 1024 * 2  # 5Mbs

    def get_file(self, db: Session, ownerid: str, fileid: str):
        return get_file_or_raise(db, ownerid, fileid, FileType.FILE)

    def get_files_in_folder(
        self,
        db: Session,
        ownerid: str,
        parentid: Optional[str],
        page: int,
        order: SortOrder,
        sort: SortColumn,
    ) -> list[FileModel]:
        column = column_and_order_from_file(sort)
        column_with_order = apply_order_to_column(order, column)

        if parentid is not None:
            file = get_file_or_raise(db, ownerid, parentid, None)

            if file.type == FileType.FILE:
                raise FileBeParent()

        query = file_by_ownerid_parentid_alive(db, ownerid, parentid)

        if parentid is not None:
            files = db.query(query.exists()).scalar()

            if files is None:
                raise ParentNotFound()

        query = query.order_by(column_with_order)
        query = query.limit(LIMIT_PER_PAGE).offset(page * LIMIT_PER_PAGE)

        return query.all()

    def download(
        self, db, ownerid: str, fileids: List[str]
    ) -> tuple[Generator[bytes, Any, None], FileModel]:
        """
        Get a stream of a file or a zip containing all files inside a folder
        """

        if len(fileids) == 0:
            raise Exception("There has to be files to download")

        file = get_file_or_raise(db, ownerid, fileids[0], None)

        if len(fileids) > 1 and file.type == FileType.FILE:
            return self._download_files(db, fileids, ownerid), file

        if file.type == FileType.FOLDER:
            return self._download_folder(db, ownerid, fileids[0]), file

        bytedata = storage_client.download(
            SUPA_BUCKETID, make_file_bucket_path(ownerid, fileids[0], "file")
        )
        stream = stream_buffer(io.BytesIO(bytedata), self.STREAM_SIZE)

        return stream, file

    def _download_files(
        self, db: Session, fileids: list[str], ownerid: str
    ) -> Generator[bytes, Any, None]:
        items = get_files(db, ownerid, fileids)
        buffer = zip_files(items, ownerid, "")
        return stream_buffer(buffer, self.STREAM_SIZE)

    def _download_folder(
        self, db: Session, ownerid: str, parentid: str
    ) -> Generator[bytes, Any, None]:
        folder = get_file_or_raise(db, ownerid, parentid, FileType.FOLDER)
        buffer = build_zip(db, ownerid, folder)
        return stream_buffer(buffer, self.STREAM_SIZE)

    def preview_file(self, db: Session, ownerid: str, id: str) -> str:
        item = get_file_or_raise(db, id, ownerid, FileType.FILE)

        bucket_path = make_file_bucket_path(ownerid, id, "preview")

        time_to_expire = 3600  # one hour
        url = storage_client.signedURL(SUPA_BUCKETID, bucket_path, time_to_expire)

        return url

    def search(
        self, db: Session, ownerid: str, query: str, type_: FileType | None
    ) -> list[FileModel]:
        user_query: Query[FileModel] = None

        user_query = search_files_by_ownerid_name_type(db, ownerid, query, type_)

        return (
            user_query.order_by(FileModel.filename.asc()).limit(LIMIT_PER_SEARCH).all()
        )

    def get_breadcrumb(self, db: Session, ownerid: str, id_: str) -> list[FileModel]:
        breadcrumb = list()

        def climb_filetree(fileid: str) -> FileModel:
            file = get_file_or_raise(db, ownerid, fileid, None)

            if file.parentid is not None:
                climb_filetree(file.parentid)

            if file.type == FileType.FILE:
                breadcrumb.append(file.filename + "." + file.extension)
            else:
                breadcrumb.append(file.filename)

        climb_filetree(id_)

        return breadcrumb
