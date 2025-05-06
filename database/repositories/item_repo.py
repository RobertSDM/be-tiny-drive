from sqlalchemy import and_, exists, update
from sqlalchemy.orm import Session, load_only

from database.models import Item


def item_by_id_ownerid(db: Session, id: str, ownerid: str) -> Item | None:
    return (
        db.query(Item)
        .options(load_only(Item.data))
        .filter(and_(Item.id == id, Item.ownerid == ownerid))
        .first()
    )


def item_exists_by_id_ownerid_parentid(
    db: Session, id: int, parentid: int, ownerid: int
) -> bool:
    return db.query(
        exists().where(
            and_(
                and_(Item.id == id, Item.parentid == parentid), Item.ownerid == ownerid
            )
        )
    ).scalar()


def create_item(db: Session, item: Item) -> Item:
    db.add(item)
    db.commit()

    return item


def item_delete(db: Session, item: Item) -> None:
    db.delete(item)
    db.commit()


def item_search(db: Session, search: str, ownerid: str) -> list[Item]:
    return (
        db.query(Item)
        .filter(
            and_(
                (Item.name + "." + Item.extension).ilike("%" + search + "%"),
                Item.ownerid == ownerid,
            )
        )
        .all()
    )


def item_by_name_parentid(
    db: Session, fullname: str, parentid: str, ownerid: str
) -> Item | None:
    return (
        db.query(Item)
        .filter(
            and_(
                and_(
                    (Item.name + "." + Item.extension) == fullname,
                    Item.parent == parentid,
                ),
                Item.ownerid == ownerid,
            )
        )
        .first()
    )


def item_by_ownerid_root(db: Session, ownerid: int) -> Item:
    return (
        db.query(Item)
        .options()
        .where(Item.ownerid == ownerid, Item.name == "root")
        .first()
    )


def items_by_ownerid(db: Session, ownerid: int) -> list[Item]:
    return db.query(Item).where(Item.ownerid == ownerid).all()


def items_by_ownerid_parentid(db: Session, ownerid: int, parentid: int) -> list[Item]:
    return (
        db.query(Item)
        .where(and_(Item.ownerid == ownerid, Item.parentid == parentid))
        .all()
    )


def items_exists_by_ownerid_parentid_path(
    db: Session, ownerid: int, parentid: int, path: str
) -> bool:
    return db.query(
        exists().where(
            and_(
                and_(Item.ownerid == ownerid, Item.parentid == parentid),
                Item.path == path,
            )
        )
    ).scalar()


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
