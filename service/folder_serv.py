from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.folder_model import Folder
from database.schemas import DefaultDefReponse, DefaultDefReponseContent
from database.repository.folder_repository import insert_folder

def save_folder_serv(db: Session, name, parent_id, owner_id) -> DefaultDefReponse | Folder:
    folder = (
        db.query(Folder)
        .filter(and_(Folder.folderC_id == parent_id, Folder.name == name))
        .first()
    )

    if folder:
        return DefaultDefReponse(
            status=422,
            content=DefaultDefReponseContent(
                msg="The name already exist in the folder",
                data=None,
            ),
        )

    folder = insert_folder(db, name, parent_id, owner_id)

    return folder
