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
    db.flush()


def item_delete(db: Session, item: FileModel) -> None:
    db.delete(item)
    db.flush()


def item_search(db: Session, search: str, ownerid: str) -> Query[FileModel]:
    return db.query(FileModel).filter(
        and_(
            (FileModel.filename + FileModel.extension).ilike("%" + search + "%"),
            FileModel.ownerid == ownerid,
        )
    )


def search_files_by_ownerid_name_type(
    db: Session, ownerid: int, query: str, type_: Optional[FileType]
) -> Query[FileModel]:
    if type_ is not None:
        return db.query(FileModel).filter(
            FileModel.ownerid == ownerid,
            FileModel.type == type_,
            FileModel.filename.ilike(f"%{query}%"),
        )

    return db.query(FileModel).filter(
        FileModel.ownerid == ownerid,
        FileModel.filename.ilike(f"%{query}%"),
    )


def file_by_ownerid_parentid_fullname_alive(
    db: Session,
    ownerid: str,
    parentid: Optional[str],
    fullname: str,
    type_: FileType = FileType.FILE,
) -> Query[FileModel]:
    query_filename = func.concat(FileModel.filename, FileModel.extension)
    if type_ == FileType.FOLDER:
        query_filename = FileModel.filename

    return db.query(FileModel).filter(
        FileModel.ownerid == ownerid,
        FileModel.parentid == parentid,
        query_filename == fullname,
        FileModel.to_delete.is_(False),
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
