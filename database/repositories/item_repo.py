from typing import Optional, TypeVar
from sqlalchemy import and_, update
from sqlalchemy.orm import Session, load_only, Query

from database.models import Item
from database.models.enums.content_type import ItemType


def item_by_id_ownerid(db: Session, id: str, ownerid: str) -> Query[Item] | None:
    return (
        db.query(Item)
        .options(load_only(Item.data))
        .filter(and_(Item.id == id, Item.ownerid == ownerid))
    )


def item_by_id(db: Session, id: int) -> Query[Item]:
    return db.query(Item).where(Item.id == id)


def item_by_id_type(db: Session, id: int, type: ItemType) -> Query[Item]:
    return db.query(Item).where(and_(Item.id == id, Item.type == type))


def item_by_ownerid_parentid_path(
    db: Session, parentid: int, ownerid: int, path: str
) -> Query[Item]:
    return db.query(Item).where(
        and_(
            and_(Item.path == path, Item.parentid == parentid), Item.ownerid == ownerid
        )
    )


def item_by_ownerid_parentid_type(
    db: Session, parentid: int, ownerid: int, type: str
) -> Query[Item]:
    return db.query(Item).where(
        and_(
            and_(Item.parentid == parentid, Item.type == type), Item.ownerid == ownerid
        )
    )


def create_item(db: Session, item: Item) -> Item:
    db.add(item)
    db.commit()

    return item


def item_delete(db: Session, item: Item) -> None:
    db.delete(item)
    db.commit()


def item_search(db: Session, search: str, ownerid: str) -> Query[Item]:
    return db.query(Item).filter(
        and_(
            (Item.name + "." + Item.extension).ilike("%" + search + "%"),
            Item.ownerid == ownerid,
        )
    )


# def item_by_name_parentid(
#     db: Session, fullname: str, parentid: str, ownerid: str
# ) -> Item | None:
#     return (
#         db.query(Item)
#         .filter(
#             and_(
#                 and_(
#                     (Item.name + "." + Item.extension) == fullname,
#                     Item.parent == parentid,
#                 ),
#                 Item.ownerid == ownerid,
#             )
#         )
#         .first()
#     )


# def item_by_ownerid(db: Session, ownerid: int) -> Item:
#     return (
#         db.query(Item)
#         .options()
#         .where(Item.ownerid == ownerid, Item.parentid == "")
#         .first()
#     )


def items_by_ownerid(db: Session, ownerid: int) -> Query[Item]:
    return db.query(Item).where(Item.ownerid == ownerid)


def items_by_ownerid_parentid(
    db: Session, ownerid: int, parentid: Optional[int]
) -> Query[Item]:
    return db.query(Item).where(
        and_(Item.ownerid == ownerid, Item.parentid == parentid)
    )


# def items_by_ownerid_path_type(
#     db: Session, ownerid: int, path: str, type: ItemType
# ) -> bool:
#     return db.query(
#         exists().where(
#             and_(
#                 and_(
#                     Item.ownerid == ownerid,
#                     Item.path == path,
#                 ),
#                 Item.type == type,
#             )
#         )
#     ).scalar()


def item_update_name(
    db: Session, name: str, id: str, ownerid: str, parentid: str
) -> None:

    (
        db.execute(
            update(Item)
            .where(
                and_(and_(Item.id == id, Item.ownerid == ownerid)),
                Item.parentid == parentid,
            )
            .values({Item.name: name})
        )
    )
    db.commit()
