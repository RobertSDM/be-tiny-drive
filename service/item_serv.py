from fastapi import Response
from sqlalchemy.orm import Session

from database.models import Item
from database.repositories.item_repo import (
    create_item,
    item_by_ownerid_root,
    items_by_ownerid_parentid,
    items_exists_by_ownerid_parentid_path,
)
from database.models.enums.content_type import ItemType
from utils import get_sufix_to_bytes


def item_create_serv(
    db: Session, name, parentid, extension, size, data, ownerid, path
) -> Item | None:
    fmtsize, prefix = get_sufix_to_bytes(size)

    if parentid == None:
        print("here")
        root = item_by_ownerid_root(db, ownerid)
        parentid = root.id

    itemexists = items_exists_by_ownerid_parentid_path(db, ownerid, parentid, path)

    print(itemexists)

    if itemexists:
        return None

    item = Item(
        name=name,
        data=data,
        extension=extension,
        size=fmtsize,
        size_prefix=prefix,
        ownerid=ownerid,
        path=path,
        parentid=parentid,
        type=ItemType.FILE.value,
    )

    return create_item(db, item)


def create_root_item(db: Session, ownerid: int):
    item = Item(
        name="root",
        data=bytes(),
        extension="",
        size=0,
        size_prefix="",
        ownerid=ownerid,
        path="/",
        parentid="",
        type=ItemType.FILE.value,
    )

    return create_item(db, item)


def get_all_root_items(db: Session, ownerid: int) -> list[Item]:
    root = item_by_ownerid_root(db, ownerid)
    return items_by_ownerid_parentid(db, ownerid, root.id)


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
