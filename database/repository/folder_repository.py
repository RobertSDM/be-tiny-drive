from sqlalchemy import and_
from service.logging_config import logger
from ..model.folder_model import Folder
from sqlalchemy.orm import load_only, joinedload, Session, selectinload


def folder_selectinload_children(db: Session, id: str, owner_id: str) -> Folder:
    folder = (
        db.query(Folder)
        .options(
            selectinload(Folder.folders).selectinload(Folder.files),
            selectinload(Folder.files),
        )
        .filter(and_(Folder.id == id, Folder.owner_id == owner_id))
        .first()
    )

    return folder


def insert_folder(db: Session, name: str, parentId: str, owner_id: str):
    try:
        if parentId:
            folder = (
                db.query(Folder)
                .options(load_only(Folder.tray))
                .filter(and_(Folder.id == parentId, Folder.owner_id == owner_id))
                .first()
            )
            parentTray = folder.tray
        else:
            parentTray = None

        folder = Folder(name, parentId, owner_id)

        db.add(folder)
        db.flush()

        folder.set_tray(parentTray)
        db.flush()

        return folder
    except Exception as e:
        logger.error(e)
        return False


def delete_folder(db: Session, folderId: str, owner_id: str):
    try:
        folder = (
            db.query(Folder)
            .options(joinedload(Folder.folder))
            .filter(and_(Folder.id == folderId, Folder.owner_id == owner_id))
            .first()
        )

        db.delete(folder)
        db.commit()

        return folder
    except Exception as e:
        logger.error(e)
        return False


def search_folder(db: Session, search: str, owner_id: str):
    folders = (
        db.query(Folder)
        .options(load_only(Folder.id, Folder.name))
        .filter(
            and_(Folder.name.ilike("%" + search + "%"), Folder.owner_id == owner_id)
        )
        .all()
    )

    return folders


def folder_by_name_in_folder(
    db: Session, name: str, folder_id: str, owner_id: str
) -> Folder | None:
    file = (
        db.query(Folder)
        .filter(
            and_(
                and_(Folder.name == name, Folder.folderC_id != folder_id),
                Folder.owner_id == owner_id,
            )
        )
        .first()
    )

    return file


def folder_update_name(
    db: Session, name: str, id: str, owner_id: str, parent_id: str
) -> str:
    if parent_id:
        parentFolder = (
            db.query(Folder)
            .options(load_only(Folder.tray))
            .filter(and_(Folder.id == parent_id, Folder.owner_id == owner_id))
            .first()
        )
        parentTray = parentFolder.tray
    else:
        parentTray = None

    folder = db.query(Folder).filter(and_(Folder.id == id, Folder.owner_id == owner_id))
    folder.update({Folder.name: name})
    db.flush()

    folder = folder.first()
    updated_tray = folder.update_tray(parentTray, name)
    db.flush()
    return updated_tray
