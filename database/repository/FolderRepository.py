from service.logging_config import logger
from ..models.FolderModel import Folder

def find_all_folders (id: str | None = None):
    pass

def save_folder (db, name):
    try:
        folder = Folder(name)

        db.add(folder)
        db.flush()

        return folder;
    except Exception as e:
        logger.error(e)
        return False
