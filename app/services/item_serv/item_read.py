import io
from typing import Any, BinaryIO, Generator
import zipfile
from sqlalchemy.orm import Session

from app.clients.supabase.storage_client import storage
from app.core.exceptions import (
    InvalidItemToPreview,
    ItemNotFound,
    ParentFolderNotFound,
)
from app.database.models import Item
from app.database.repositories.item_repo import (
    item_by_id_ownerid,
    item_by_ownerid_parentid,
    items_by_ownerid_name,
    items_by_ownerid_name_type,
)
from app.constants.env_ import drive_bucketid
from app.enums.enums import ItemType
from app.utils.execute_query import (
    execute_all,
    execute_first,
    paginate,
    query_pipe,
)
from app.utils.utils import make_bucket_path
from app.constants.database_variables import limit_per_page


class _ItemReadServ:

    def all_root_items_serv(self, db: Session, ownerid: str, page: int) -> list[Item]:
        pipe = query_pipe(
            item_by_ownerid_parentid,
            lambda query: paginate(query, limit_per_page, page),
            execute_all,
        )
        return pipe(db, ownerid, None)

    def item_by_id_serv(self, db: Session, ownerid: str, id: str):
        item = execute_first(item_by_id_ownerid(db, id, ownerid))

        if not item:
            raise ItemNotFound()

        return item

    def all_items_in_folder_serv(self, db: Session, ownerid: str, parentid: str | None):
        return execute_all(item_by_ownerid_parentid(db, ownerid, parentid))

    def download_serv(self, db, id: str, ownerid: str) -> str:
        item = execute_first(item_by_id_ownerid(db, id, ownerid))

        if not item:
            raise ItemNotFound()

        if item.type == ItemType.FILE:
            bucket_item_path = make_bucket_path(item)
            url = storage.signedURL(
                drive_bucketid, bucket_item_path, 5 * 60, f"{item.name}{item.extension}"
            )

            return url

        return ""

    def _create_list_to_download(
        self, db: Session, ownerid: str, fileids: list[str]
    ) -> list[Item]:
        to_download = list()

        for id in fileids:
            item = execute_first(item_by_id_ownerid(db, id, ownerid))
            if not item:
                raise ItemNotFound()

            to_download.append(item)

        return to_download

    def _zip_items(self, items: list[Item]) -> io.BytesIO:
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip:
            for item in items:
                try:
                    file = storage.download(
                        drive_bucketid,
                        make_bucket_path(item),
                    )

                    zip.writestr(f"{item.name}{item.extension}", file)

                except Exception as e:
                    raise e

        buffer.seek(0)
        return buffer

    def _gen_zip_path(self, initpath: str, name: str) -> str:
        return (f"{initpath}/" if len(initpath) > 0 else "") + name

    def _stream_buffer(self, buffer: BinaryIO) -> Generator[bytes, Any, None]:
        while 1:
            b = buffer.read(5 * (1024 * 1024))  # 5mbs
            if len(b) == 0:
                break
            yield b

    def _build_folder_zip(self, db: Session, ownerid: str, root: Item):
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip:
            self._dfs_zip_items(db, ownerid, zip, root, root.name)

        buffer.seek(0)
        return buffer

    def _dfs_zip_items(
        self, db: Session, ownerid: str, zip: zipfile.ZipFile, folder: Item, path: str
    ) -> io.BytesIO:
        items = execute_all(item_by_ownerid_parentid(db, ownerid, folder.id))

        for item in items:
            if item.type == ItemType.FILE:
                try:
                    file = storage.download(
                        drive_bucketid,
                        make_bucket_path(item),
                    )

                    file_path = self._gen_zip_path(path, f"{item.name}{item.extension}")
                    zip.writestr(
                        file_path,
                        file,
                    )

                except Exception as e:
                    raise e
            else:
                folder_path = self._gen_zip_path(path, item.name)
                self._dfs_zip_items(db, ownerid, zip, item, folder_path)

    def download_many_serv(
        self, db: Session, fileids: list[str], ownerid: str
    ) -> Generator[bytes, Any, None]:
        items = self._create_list_to_download(db, ownerid, fileids)
        buffer = self._zip_items(items)
        yield from self._stream_buffer(buffer)

    def _get_folder_or_raise(self, db: Session, ownerid: str, id: str) -> Item:
        folder = execute_first(item_by_id_ownerid(db, id, ownerid))

        if not folder:
            raise ParentFolderNotFound()

        return folder

    def download_folder_serv(
        self, db: Session, ownerid: str, parentid: str
    ) -> Generator[bytes, Any, None]:
        folder = self._get_folder_or_raise(db, ownerid, parentid)
        buffer = self._build_folder_zip(db, ownerid, folder)
        print(buffer)
        yield from self._stream_buffer(buffer)

    def image_preview_serv(self, db: Session, ownerid: str, id: str) -> str:
        item = execute_first(item_by_id_ownerid(db, id, ownerid))

        if not item:
            raise ItemNotFound()

        if not item.content_type.startswith("image"):
            raise InvalidItemToPreview()

        try:
            bucket_item_path = make_bucket_path(item)
            url = storage.signedURL(drive_bucketid, bucket_item_path, 3600)
        except Exception as e:
            raise e
        return url

    def search_serv(
        self, db: Session, ownerid: str, query: str, type: ItemType | None
    ) -> list[Item]:
        if type:
            items = execute_all(items_by_ownerid_name_type(db, ownerid, query, type))
        else:
            items = execute_all(items_by_ownerid_name(db, ownerid, query))
        return items

    def _climb_file_tree(self, db: Session, ownerid: str, parentid: str) -> list[Item]:

        item = self._get_folder_or_raise(db, ownerid, parentid)
        if not item.parentid:
            return [item]
        res = [item]

        res.extend(self._climb_file_tree(db, ownerid, item.parentid))

        return res

    def breadcrumb_serv(self, db: Session, ownerid: str, id: str) -> list[Item]:
        breadcrumb = self._climb_file_tree(db, ownerid, id)

        breadcrumb.reverse()
        return breadcrumb


item_read_serv = _ItemReadServ()
