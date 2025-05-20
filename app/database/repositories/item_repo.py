from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from ..models import Item
from app.enums.enums import ItemType


def item_by_id_ownerid(db: Session, id: str, ownerid: str) -> Query[Item]:
    return db.query(Item).where(and_(Item.id == id, Item.ownerid == ownerid))


def item_by_ownerid_path(db: Session, ownerid: str, path: str) -> Query[Item]:
    return db.query(Item).where(and_(Item.path == path, Item.ownerid == ownerid))


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


def items_by_ownerid_name_type(
    db: Session, ownerid: int, query: str, type: ItemType
) -> Query[Item]:
    return db.query(Item).where(
        and_(
            and_(Item.ownerid == ownerid, Item.type == type),
            Item.name.ilike(f"%{query}%"),
        )
    )


def items_by_ownerid_name(db: Session, ownerid: int, query: str) -> Query[Item]:
    return db.query(Item).where(
        and_(
            Item.ownerid == ownerid,
            Item.name.ilike(f"%{query}%"),
        )
    )


def item_by_ownerid_parentid(
    db: Session, ownerid: str, parentid: Optional[str]
) -> Query[Item]:
    return db.query(Item).where(
        and_(Item.ownerid == ownerid, Item.parentid == parentid)
    )
