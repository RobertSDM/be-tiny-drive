from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.FolderModel import Folder
from database.schemas.schemas import DefaultDefReponse, DefaultDefReponseContent


def save_folder(db: Session, name, parent_id, owner_id) -> DefaultDefReponse | Folder:
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

    folder = save_folder(db, name, parent_id, owner_id)

    return folder
