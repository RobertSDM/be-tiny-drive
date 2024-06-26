from service.logging_config import logger
from ..models.FolderModel import Folder
from sqlalchemy.orm import load_only, joinedload, Session

def find_all_folders (id: str | None = None):
    pass

def save_folder (db, name, parentId):
    try:
        
        if(parentId):
            folder = db.query(Folder).options(load_only(Folder.tray)).filter(Folder.id == parentId).first()
            parentTray = folder.tray
        else:
            parentTray = None
        
        folder = Folder(name, parentId)

        db.add(folder)
        db.flush()

        folder.set_tray(parentTray)
        db.flush()

        print("TRAY : " + folder.tray);

        return folder;
    except Exception as e:
        logger.error(e)
        return False

        
def delete_folder(db: Session, folderId):
    try:
        folder = db.query(Folder).options(joinedload(Folder.folder)).filter(Folder.id == folderId).first()

        db.delete(folder)
        db.commit()

        return folder
    except Exception as e:
        logger.error(e)
        return False
