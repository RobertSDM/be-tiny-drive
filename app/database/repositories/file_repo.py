from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, Query


from ..models import FileModel


def file_by_id_ownerid(db: Session, id: str, ownerid: str) -> Query[FileModel]:
    return db.query(FileModel).filter(FileModel.id == id, FileModel.ownerid == ownerid)


def file_by_id_ownerid_active(db: Session, id: str, ownerid: str) -> Query[FileModel]:
    return db.query(FileModel).filter(
        FileModel.id == id,
        FileModel.ownerid == ownerid,
    )


def file_by_id_ownerid_is_dir(
    db: Session, id: str, ownerid: str, is_dir: bool
) -> Query[FileModel]:
    return db.query(FileModel).filter(
        FileModel.id == id,
        FileModel.ownerid == ownerid,
        FileModel.is_dir.is_(is_dir),
    )


def file_save(db: Session, file: FileModel) -> FileModel:
    db.add(file)
    db.flush()


def file_delete(db: Session, file: FileModel) -> None:
    db.delete(file)
    db.flush()


def search_files_by_ownerid_name_is_dir(
    db: Session, ownerid: int, query: str, is_dir: Optional[bool]
) -> Query[FileModel]:
    if is_dir is not None:
        return db.query(FileModel).filter(
            FileModel.ownerid == ownerid,
            FileModel.is_dir.is_(is_dir),
            FileModel.filename.ilike(f"%{query}%"),
        )

    return db.query(FileModel).filter(
        FileModel.ownerid == ownerid,
        FileModel.filename.ilike(f"%{query}%"),
    )


def file_by_ownerid_parentid_fullname(
    db: Session,
    ownerid: str,
    parentid: Optional[str],
    fullname: str,
    is_dir: bool = False,
) -> Query[FileModel]:
    query_filename = func.concat(FileModel.filename, FileModel.extension)
    if is_dir:
        query_filename = FileModel.filename

    return db.query(FileModel).filter(
        FileModel.ownerid == ownerid,
        FileModel.parentid == parentid,
        query_filename == fullname,
    )


def file_by_ownerid_parentid(
    db: Session, ownerid: str, parentid: Optional[str]
) -> Query[FileModel]:
    return db.query(FileModel).filter(
        FileModel.ownerid == ownerid, FileModel.parentid == parentid
    )


def file_by_ownerid_parentid_type(
    db: Session, ownerid: str, parentid: Optional[str], is_dir: bool
) -> Query[FileModel]:
    return db.query(FileModel).filter(
        FileModel.ownerid == ownerid,
        FileModel.parentid == parentid,
        FileModel.is_dir.is_(is_dir),
    )
