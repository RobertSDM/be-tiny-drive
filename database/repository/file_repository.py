import json
from sqlalchemy.orm import joinedload, Session, load_only, lazyload, selectinload
from sqlalchemy import and_, update
from service.logging_config import logger
from database.model.folder_model import Folder
from ..model.file_model import File


## Not beeing used
# def find_all_files(db):
#     return db.query(File).options(joinedload(File.fileData)).all()


def download_file(db: Session, id: str, owner_id: str):

    file = (
        db.query(File   )
        .options(load_only(File.id), selectinload(File.fileData))
        .filter(and_(File.id == id, File.owner_id == owner_id))
        .first()
    )

    return file


def insert_file(
    db: Session,
    name: str,
    extension: str,
    byteData: str,
    byteSize: int,
    prefix: str,
    owner_id: str,
    folderId: str,
):

    file = File(name, extension, byteSize, prefix, byteData, folderId, owner_id)

    db.add(file)
    db.flush()

    return file


def delete_file(db: Session, id: str, owner_id: str):
    try:
        file = (
            db.query(File)
            .options(joinedload(File.folder))
            .where(and_(File.id == id, File.owner_id == owner_id))
            .first()
        )

        db.delete(file)
        db.commit()

        return file
    except Exception as e:
        logger.error(e)
        return False


def search_file(db: Session, search: str, owner_id: str):
    files = (
        db.query(File)
        .options(
            load_only(
                File.id,
                File.extension,
                File.name,
            )
        )
        .filter(and_(File.name.ilike("%" + search + "%"), File.owner_id == owner_id))
        .all()
    )

    return files


def file_by_name_in_folder(
    db: Session, fullname: str, folder_id: str, owner_id: str
) -> File | None:
    file = (
        db.query(File)
        .filter(
            and_(
                and_(File.fullname == fullname, File.folder_id == folder_id),
                File.owner_id == owner_id,
            )
        )
        .first()
    )

    return file


def file_update_name(
    db: Session, fullname: str, name: str, id: str, owner_id: str, folder_id: str
) -> None:
    (
        db.execute(
            update(File)
            .where(
                and_(and_(File.id == id, File.owner_id == owner_id)),
                File.folder_id == folder_id,
            )
            .values({File.name: name, File.fullname: fullname})
        )
    )

    db.commit()
