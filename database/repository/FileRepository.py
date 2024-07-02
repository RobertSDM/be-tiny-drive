from sqlalchemy.orm import joinedload, Session, load_only, lazyload, joinedload
from sqlalchemy import select, and_
from service.logging_config import logger
from database.models.FolderModel import Folder
from ..models.FileModel import File, FileData


def find_all_files(db):
    return db.query(File).options(joinedload(File.fileData)).all()


def find_by_file_id_download(db, id):

    fileData_subq = (
        select(FileData.byteData, FileData.file_id).select_from(FileData).subquery()
    )

    file_join_fileData = (
        select(File.id, File.fullname, fileData_subq.c.byteData)
        .join(fileData_subq, File.id == fileData_subq.c.file_id)
        .where(File.id == id)
    )

    file = db.execute(file_join_fileData).mappings().fetchone()

    return file


def save_file(
    db,
    name,
    extension,
    byteData,
    byteSize,
    prefix,
    owner_id,
    folderId: str,
):

    file = File(name, extension, byteSize, prefix, byteData, folderId, owner_id)

    db.add(file)
    db.flush()

    return file


def files_with_no_parent(db: Session, owner_id: str) -> list:

    files = (
        db.query(File)
        .options(
            load_only(
                File.id,
                File.extension,
                File.name,
                File.byteSize,
                File.fullname,
                File.prefix,
            ),
            lazyload(File.fileData),
        )
        .filter(and_(File.folder_id == None, File.owner_id == owner_id))
        .all()
    )

    folders = (
        db.query(Folder)
        .where(and_(Folder.folderC_id == None, Folder.owner_id == owner_id))
        .all()
    )

    return {"files": files, "folders": folders}


def files_by_folder(db: Session, folderId: str, owner_id: str) -> list:

    requestedFolder = (
        db.query(Folder)
        .options(
            load_only(Folder.id, Folder.name, Folder.tray, Folder.folderC_id),
            joinedload(Folder.folder),
        )
        .filter(and_(Folder.id == folderId, Folder.owner_id == owner_id))
        .first()
    )

    files = (
        db.query(File)
        .options(
            load_only(
                File.id,
                File.extension,
                File.name,
                File.byteSize,
                File.fullname,
                File.prefix,
            )
        )
        .filter(and_(File.folder_id == folderId, File.owner_id == owner_id))
        .all()
    )

    folders = (
        db.query(Folder)
        .options(
            load_only(Folder.id, Folder.name, Folder.tray, Folder.folderC_id),
            joinedload(Folder.folder),
        )
        .filter(and_(Folder.folderC_id == folderId, Folder.owner_id == owner_id))
        .all()
    )

    return {"files": files, "folders": folders, "requestedFolder": requestedFolder}


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
