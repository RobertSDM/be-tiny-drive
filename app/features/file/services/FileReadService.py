import io
from typing import Any, Generator, List
from sqlalchemy.orm import Session, Query

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
from app.core.exceptions import (
    FileNotFound,
)
from app.database.models import FileModel
from app.database.repositories.item_repo import (
    file_by_id_ownerid,
    file_by_ownerid_parentid_alive,
    items_by_ownerid_name,
    items_by_ownerid_name_type,
)
from app.core.constants import SUPA_BUCKETID
from app.core.schemas import FileType, SortColumn, SortOrder
from app.utils.utils import (
    make_file_bucket_path,
    get_file_preview_bucket_path,
)
from app.core.constants import LIMIT_PER_PAGE, LIMIT_PER_SEARCH


class FileReadService:

    def __init__(self):
        self.STREAM_SIZE = 5 * 1024 * 2  # 5Mbs

    def get_files(
        self, db: Session, ownerid: str, page: int, order: SortOrder, sort: SortColumn
    ) -> list[FileModel]:
        return self.get_files_in_folder(db, ownerid, None, page, order, sort)

    def get_file(self, db: Session, ownerid: str, fileid: str):
        return get_file_or_raise(db, ownerid, fileid, FileType.FILE)

    def get_files_in_folder(
        self,
        db: Session,
        ownerid: str,
        parentid: str | None,
        page: int,
        order: SortOrder,
        sort: SortColumn,
    ) -> list[FileModel]:
        column = column_and_order_from_file(sort)
        column_with_order = apply_order_to_column(order, column)

        query = file_by_ownerid_parentid_alive(db, ownerid, parentid)
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

        file = file_by_id_ownerid(db, fileids[0], ownerid).first()

        if not file:
            raise FileNotFound()

        if file.type == FileType.FILE and len(fileids) > 0:
            return self._download_files(db, fileids, ownerid), file

        if file.type == FileType.FOLDER:
            return self._download_folder(db, ownerid, fileids[0]), file

        file = storage_client.download(SUPA_BUCKETID, make_file_bucket_path(file))
        stream = stream_buffer(io.BytesIO(file), self.STREAM_SIZE)

        return stream(), file

    def _download_files(
        self, db: Session, fileids: list[str], ownerid: str
    ) -> Generator[bytes, Any, None]:
        items = get_files(db, ownerid, fileids)
        buffer = zip_files(items)
        yield from stream_buffer(buffer, self.STREAM_SIZE)

    def _download_folder(
        self, db: Session, ownerid: str, parentid: str
    ) -> Generator[bytes, Any, None]:
        folder = get_file_or_raise(db, ownerid, parentid, FileType.FOLDER)
        buffer = build_zip(db, ownerid, folder)
        yield from stream_buffer(buffer, self.STREAM_SIZE)

    def preview_file(self, db: Session, ownerid: str, id: str) -> str:
        item = get_file_or_raise(db, id, ownerid, FileType.FILE)

        bucket_path = get_file_preview_bucket_path(item)

        time_to_expire = 3600  # one hour
        url = storage_client.signedURL(SUPA_BUCKETID, bucket_path, time_to_expire)

        return url

    def search(
        self, db: Session, ownerid: str, user_query: str, type_: FileType | None
    ) -> list[FileModel]:
        user_query: Query[FileModel] = None

        if type_:
            user_query = items_by_ownerid_name_type(db, ownerid, user_query, type_)
        else:
            user_query = items_by_ownerid_name(db, ownerid, user_query)

        return user_query.limit(LIMIT_PER_SEARCH).all()

    def get_breadcrumb(self, db: Session, ownerid: str, id: str) -> list[FileModel]:
        file = get_file_or_raise(db, ownerid, id)
        return file.path
