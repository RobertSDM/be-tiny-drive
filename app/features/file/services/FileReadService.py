import io
from typing import Any, Generator, List, Optional
from sqlalchemy.orm import Session, Query
from storage3.exceptions import StorageApiError

from app.core.exceptions import (
    FileNotBeParent,
    FolderNotFound,
    PreviewNotFound,
    PreviewNotSupported,
)
from app.features.file.utils import (
    apply_order_to_column,
    file_exists_or_raise,
    zip_folder,
    column_from_sort,
    get_file_or_raise,
    get_files,
    zip_files,
    stream_buffer,
)
from app.lib.supabase.storage import supabase_storage_client

from app.database.models import FileModel
from app.database.repositories.file_repo import (
    file_by_ownerid_parentid,
    search_files_by_ownerid_name_is_dir,
)
from app.core.constants import SUPA_BUCKETID, SUPPORTED_PREVIEW_TYPES
from app.core.schemas import BreadcrumbResponse, SortColumn, SortOrder
from app.utils.utils import (
    make_file_bucket_path,
)
from app.core.constants import LIMIT_PER_PAGE, LIMIT_PER_SEARCH


class FileReadService:

    def __init__(self):
        self.STREAM_SIZE = 5 * 1024 * 2  # 5Mbs

    def get_file(self, db: Session, ownerid: str, fileid: str):
        return get_file_or_raise(db, ownerid, fileid, False)

    def get_files_in_folder(
        self,
        db: Session,
        ownerid: str,
        parentid: Optional[str],
        page: int,
        order: SortOrder,
        sort: SortColumn,
    ) -> list[FileModel]:
        column_with_order = apply_order_to_column(order, column_from_sort(sort))

        if parentid is not None:
            file = get_file_or_raise(db, ownerid, parentid, None)

            if not file.is_dir:
                raise FileNotBeParent()

        query = file_by_ownerid_parentid(db, ownerid, parentid)

        if parentid is not None:
            files = db.query(query.exists()).scalar()

            if files is None:
                raise FolderNotFound()

        query = query.order_by(column_with_order)
        query = query.limit(LIMIT_PER_PAGE).offset(page * LIMIT_PER_PAGE)

        return query.all()

    def download(
        self, db, ownerid: str, fileids: List[str]
    ) -> tuple[Generator[bytes, Any, None], FileModel]:
        """
        Returns a stream of a file or a zip containing all files inside a folder
        """

        if len(fileids) == 0:
            raise Exception("There isn't files to download")

        file = get_file_or_raise(db, ownerid, fileids[0], None)

        if len(fileids) > 1 and not file.is_dir:
            return self._download_files(db, fileids, ownerid), file

        if file.is_dir:
            return self._download_folder(db, ownerid, fileids[0]), file

        bytedata = supabase_storage_client.download(
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
        folder = get_file_or_raise(db, ownerid, parentid, True)
        buffer = zip_folder(db, ownerid, folder)
        return stream_buffer(buffer, self.STREAM_SIZE)

    def preview(self, db: Session, ownerid: str, id_: str) -> str:
        file = get_file_or_raise(db, ownerid, id_)

        if file.content_type not in SUPPORTED_PREVIEW_TYPES:
            raise PreviewNotSupported()

        bucket_path = make_file_bucket_path(ownerid, id_, "preview")

        time_to_expire = 3600  # one hour
        try:
            return supabase_storage_client.signedURL(
                SUPA_BUCKETID, bucket_path, time_to_expire
            )
        except StorageApiError as e:
            if e.code == "NoSuchUpload":
                raise PreviewNotFound()

    def search(
        self, db: Session, ownerid: str, query: str, is_dir: Optional[bool]
    ) -> list[FileModel]:
        user_query: Query[FileModel] = None

        user_query = search_files_by_ownerid_name_is_dir(db, ownerid, query, is_dir)

        return (
            user_query.order_by(FileModel.filename.asc()).limit(LIMIT_PER_SEARCH).all()
        )

    def get_breadcrumb(
        self, db: Session, ownerid: str, id_: str
    ) -> List[BreadcrumbResponse]:
        breadcrumb: List[BreadcrumbResponse] = list()

        def climb_filetree(fileid: str) -> FileModel:
            file = get_file_or_raise(db, ownerid, fileid, None)

            if file.parentid is not None:
                climb_filetree(file.parentid)

            if not file.is_dir:
                breadcrumb.append(
                    BreadcrumbResponse(
                        id=file.id, filename=file.filename + file.extension
                    )
                )
            else:
                breadcrumb.append(
                    BreadcrumbResponse(id=file.id, filename=file.filename)
                )

        climb_filetree(id_)

        return breadcrumb
