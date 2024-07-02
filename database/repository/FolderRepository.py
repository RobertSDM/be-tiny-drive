from sqlalchemy import and_
from service.logging_config import logger
from ..models.FolderModel import Folder
from sqlalchemy.orm import load_only, joinedload, Session


def save_folder(db, name: str, parentId: str, owner_id: str):
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
