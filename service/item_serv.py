from sqlalchemy.orm import Session

from core.exeptions import ItemExistsInFolder, ParentFolderNotFound
from database.models import Item
from database.repositories import (
    create_item,
    items_by_ownerid_parentid,
)
from database.models.enums.content_type import ItemType
from database.repositories import (
    execute_exists,
    execute_first,
)
from database.repositories.item_repo import (
    item_by_id_type,
    item_by_ownerid_parentid_path,
)
from database.repositories.utils import execute_all
from utils import get_sufix_to_bytes


def item_create_serv(
    db: Session,
    name: str,
    parentid: int,
    extension: str,
    size: int,
    data: bytes,
    ownerid: int,
    path: str,
    type: ItemType,
) -> Item:
    fmtsize, prefix = get_sufix_to_bytes(size)

    if parentid == None or parentid == "":
        root = execute_first(db, items_by_ownerid_parentid(db, ownerid, None))
        parentid = root.id

    item_exists = execute_exists(
        db, item_by_ownerid_parentid_path(db, ownerid, parentid, path)
    )

    if item_exists:
        raise ItemExistsInFolder(name, type.value)

    parent_exists = execute_exists(
        db, item_by_id_type(db, parentid, ItemType.FOLDER.value)
    )

    if not parent_exists:
        raise ParentFolderNotFound()

    item = Item(
        name=name,
        data=data,
        extension=extension,
        size=fmtsize,
        size_prefix=prefix,
        ownerid=ownerid,
        path=path,
        parentid=parentid,
        type=type,
    )

    return create_item(db, item)


def create_root_item(db: Session, ownerid: int) -> Item:
    item = Item(
        name="root",
        data=bytes(),
        extension="",
        size=0,
        size_prefix="",
        ownerid=ownerid,
        path="/",
        parentid=None,
        type=ItemType.FOLDER.value,
    )

    return create_item(db, item)


def get_all_root_items(db: Session, ownerid: int) -> list[Item]:
    root = execute_first(db, items_by_ownerid_parentid(db, ownerid, None))
    return execute_all(db, items_by_ownerid_parentid(db, ownerid, root.id))


# def download_serv(db, id, owner_id):
#     data = download_file(db, id, owner_id)
#     # byte_data = get_bytes_data()
#     return [data, data.fileData.byteData]


# def update_file_name_serv(
#     db: Session, file_id: str, body: FileUpdate, owner_id: str
# ) -> DefaultDefReponse | bool:

#     fullname = body.new_name + "." + body.extension

#     exist = file_by_name_in_folder(db, fullname, body.folder_id, owner_id)

#     if exist:
#         return DefaultDefReponse(
#             status=422,
#             content=DefaultDefReponseContent(
#                 msg="Can't update the file \""
#                 + addThreePeriods(body.name, 30)
#                 + '" to "'
#                 + addThreePeriods(body.new_name, 30)
#                 + '" the name already exist in the folder',
#                 data=None,
#             ),
#         )

#     file_update_name(db, fullname, body.new_name, file_id, owner_id, body.folder_id)

#     return True
