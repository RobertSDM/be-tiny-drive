from sqlalchemy.orm import Session

from database.repositories.file_repository import search_file
from database.repositories.folder_repository import search_folder
from model.enums.content_type import ItemType


def content_search_serv(
    db: Session, search: str, owner_id: str, type: ItemType | None = None
):

    files = []
    folders = []

    if type == ItemType.FILE.value:
        files = search_file(db, search, owner_id)

        return {"files": files, "folders": folders}
    elif type == ItemType.FOLDER.value:
        folders = search_folder(db, search, owner_id)

        return {"files": files, "folders": folders}
    else:
        files = search_file(db, search, owner_id)
        folders = search_folder(db, search, owner_id)

        return {"files": files, "folders": folders}
