from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from ..models import Item
from app.utils.enums import ItemType


def item_by_id_ownerid(db: Session, id: str, ownerid: str) -> Query[Item]:
    return db.query(Item).where(and_(Item.id == id, Item.ownerid == ownerid))


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


def item_save(db: Session, item: Item) -> Item:
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


def items_by_ownerid(db: Session, ownerid: int) -> Query[Item]:
    return db.query(Item).where(Item.ownerid == ownerid)


def item_by_ownerid_parentid(
    db: Session, ownerid: int, parentid: Optional[int]
) -> Query[Item]:
    return db.query(Item).where(
        and_(Item.ownerid == ownerid, Item.parentid == parentid)
    )
