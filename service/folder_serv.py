import io
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.folder_model import Folder
from database.schemas import (
    DefaultDefReponse,
    DefaultDefReponseContent,
    FolderUpdate,
    UpdatedTray,
)
from database.repository.folder_repository import (
    folder_by_name_in_folder,
    folder_selectinload_children,
    folder_update_name,
    insert_folder,
)
from utils.add_three_periods import addThreePeriods
from utils.folder_to_zip import get_folder_zip


def download_zip_serv(db: Session, folder_id: str, owner_id: str) -> io.BytesIO:
    folder = folder_selectinload_children(db, folder_id, owner_id)

    return get_folder_zip(folder)


def save_folder_serv(
    db: Session, name, parent_id, owner_id
) -> DefaultDefReponse | Folder:
    folder = (
        db.query(Folder)
        .filter(
            and_(
                and_(Folder.folderC_id == parent_id, Folder.name == name),
                Folder.owner_id == owner_id,
            )
        )
        .first()
    )

    if folder:
        return DefaultDefReponse(
            status=422,
            content=DefaultDefReponseContent(
                msg="The folder \""
                + addThreePeriods(folder.name, 30)
                + "\" already exist in the folder",
                data=None,
            ),
        )

    folder = insert_folder(db, name, parent_id, owner_id)

    return folder


def update_folder_name_serv(
    db: Session, file_id: str, body: FolderUpdate, owner_id: str
) -> DefaultDefReponse | UpdatedTray:

    exist = folder_by_name_in_folder(db, body.name, body.folder_id, owner_id)

    if exist:
        return DefaultDefReponse(
            status=422,
            content=DefaultDefReponseContent(
                msg="Can't update the file \""
                + addThreePeriods(body.name, 30)
                + '" the name.extension already exist in the folder',
                data=None,
            ),
        )

    updatedTray = folder_update_name(
        db, body.new_name, file_id, owner_id, body.parent_id
    )

    return updatedTray
