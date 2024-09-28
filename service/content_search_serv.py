from sqlalchemy.orm import Session

from database.repository.file_repository import search_file
from database.repository.folder_repository import search_folder
from model.enums.content_type import Content_type


def content_search_serv(
    db: Session, search: str, owner_id: str, type: Content_type | None = None
):

    files = []
    folders = []

    if type == Content_type.FILE.value:
        files = search_file(db, search, owner_id)

        return {"files": files, "folders": folders}
    elif type == Content_type.FOLDER.value:
        folders = search_folder(db, search, owner_id)

        return {"files": files, "folders": folders}
    else:
        files = search_file(db, search, owner_id)
        folders = search_folder(db, search, owner_id)

        return {"files": files, "folders": folders}
