from typing import Optional
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, Query


from ..models import FileModel
from app.core.schemas import FileType


def file_by_id_ownerid(db: Session, id: str, ownerid: str) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(FileModel.id == id, FileModel.ownerid == ownerid)
    )


def file_by_id_ownerid_active(db: Session, id: str, ownerid: str) -> Query[FileModel]:
    return db.query(FileModel).where(
        FileModel.id == id,
        FileModel.ownerid == ownerid,
        FileModel.to_delete.is_(False),
    )


def item_by_id_ownerid_type(
    db: Session, id: str, ownerid: str, type: FileType
) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(
            and_(FileModel.id == id, FileModel.ownerid == ownerid),
            FileModel.type == type,
        )
    )


def item_by_ownerid_parentid_fullname(
    db: Session, ownerid: str, path: str
) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(FileModel.path == path, FileModel.ownerid == ownerid)
    )


def item_save(db: Session, item: FileModel) -> FileModel:
    db.add(item)
    db.commit()
    return item


def item_delete(db: Session, item: FileModel) -> None:
    db.delete(item)
    db.commit()


def item_search(db: Session, search: str, ownerid: str) -> Query[FileModel]:
    return db.query(FileModel).filter(
        and_(
            (FileModel.filename + "." + FileModel.extension).ilike("%" + search + "%"),
            FileModel.ownerid == ownerid,
        )
    )


def items_by_ownerid_name_type(
    db: Session, ownerid: int, query: str, type: FileType
) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(
            FileModel.ownerid == ownerid,
            FileModel.type == type,
            FileModel.filename.ilike(f"%{query}%"),
        ),
    )


def items_by_ownerid_name(db: Session, ownerid: int, query: str) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(
            FileModel.ownerid == ownerid,
            FileModel.filename.ilike(f"%{query}%"),
        )
    )


def file_by_ownerid_parentid_fullname_alive(
    db: Session, ownerid: str, parentid: Optional[str], fullname: str
) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(
            FileModel.ownerid == ownerid,
            FileModel.parentid == parentid,
            func.concat(FileModel.filename, ".", FileModel.extension) == fullname,
            FileModel.to_delete.is_(False),
        ),
    )


def item_by_ownerid_parentid(
    db: Session, ownerid: str, parentid: Optional[str]
) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(FileModel.ownerid == ownerid, FileModel.parentid == parentid)
    )


def file_by_ownerid_parentid_alive(
    db: Session, ownerid: str, parentid: Optional[str]
) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(
            FileModel.ownerid == ownerid,
            FileModel.parentid == parentid,
            FileModel.to_delete == False,
        )
    )


def item_by_ownerid_parentid_type(
    db: Session, ownerid: str, parentid: Optional[str], type: FileType
) -> Query[FileModel]:
    return db.query(FileModel).where(
        and_(
            FileModel.ownerid == ownerid,
            FileModel.parentid == parentid,
            FileModel.type == type,
        )
    )
