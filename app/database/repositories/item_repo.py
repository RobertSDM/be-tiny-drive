from typing import Optional
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, Query


from ..models import File
from app.core.schemas import FileType


def item_by_id_ownerid(db: Session, id: str, ownerid: str) -> Query[File]:
    return db.query(File).where(and_(File.id == id, File.ownerid == ownerid))


def item_by_id_ownerid_type(
    db: Session, id: str, ownerid: str, type: FileType
) -> Query[File]:
    return db.query(File).where(
        and_(and_(File.id == id, File.ownerid == ownerid), File.type == type)
    )


def item_by_ownerid_parentid_fullname(
    db: Session, ownerid: str, path: str
) -> Query[File]:
    return db.query(File).where(and_(File.path == path, File.ownerid == ownerid))


def item_save(db: Session, item: File) -> File:
    db.add(item)
    db.commit()
    return item


def item_delete(db: Session, item: File) -> None:
    db.delete(item)
    db.commit()


def item_search(db: Session, search: str, ownerid: str) -> Query[File]:
    return db.query(File).filter(
        and_(
            (File.filename + "." + File.extension).ilike("%" + search + "%"),
            File.ownerid == ownerid,
        )
    )


def items_by_ownerid_name_type(
    db: Session, ownerid: int, query: str, type: FileType
) -> Query[File]:
    return db.query(File).where(
        and_(
            File.ownerid == ownerid,
            File.type == type,
            File.filename.ilike(f"%{query}%"),
        ),
    )


def items_by_ownerid_name(db: Session, ownerid: int, query: str) -> Query[File]:
    return db.query(File).where(
        and_(
            File.ownerid == ownerid,
            File.filename.ilike(f"%{query}%"),
        )
    )


def item_by_ownerid_parentid_fullname(
    db: Session, ownerid: str, parentid: Optional[str], fullname: str
) -> Query[File]:
    return db.query(File).where(
        and_(
            File.ownerid == ownerid,
            File.parentid == parentid,
            (File.filename + File.extension) == fullname,
        ),
    )


def item_by_ownerid_parentid_fullname_non_deleted(
    db: Session, ownerid: str, parentid: Optional[str], fullname: str
) -> Query[File]:
    return db.query(File).where(
        and_(
            File.ownerid == ownerid,
            File.parentid == parentid,
            func.concat(File.filename, File.extension) == fullname,
            File.to_delete.is_(False),
        ),
    )


def item_by_ownerid_parentid(
    db: Session, ownerid: str, parentid: Optional[str]
) -> Query[File]:
    return db.query(File).where(
        and_(File.ownerid == ownerid, File.parentid == parentid)
    )


def item_by_ownerid_parentid_non_deleted(
    db: Session, ownerid: str, parentid: Optional[str]
) -> Query[File]:
    return db.query(File).where(
        and_(
            File.ownerid == ownerid, File.parentid == parentid, File.to_delete == False
        )
    )


def item_by_ownerid_parentid_type(
    db: Session, ownerid: str, parentid: Optional[str], type: FileType
) -> Query[File]:
    return db.query(File).where(
        and_(File.ownerid == ownerid, File.parentid == parentid, File.type == type)
    )
