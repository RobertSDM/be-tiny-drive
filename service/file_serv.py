import json
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.file_model import File, FileData
from database.repositories.folder_repository import folder_by_id
from database.repositories.user_repository import user_by_id
from schemas.schemas import DefaultDefReponse, DefaultDefReponseContent, FileUpdate
from utils import get_sufix_to_bytes
from database.repositories.file_repository import (
    file_by_name_in_folder,
    file_update_name,
    file_by_folderid_and_fullname_and_ownerid,
    insert_file,
    download_file,
)
from utils import addThreePeriods


def save_file_serv(
    db: Session, name, folderId, extension, byteData, byteSize, owner_id
) -> DefaultDefReponse | File:
    file = file_by_folderid_and_fullname_and_ownerid(
        db, f"{name}.{extension}", folderId, owner_id
    )

    if file:
        return DefaultDefReponse(
            status=422,
            content=DefaultDefReponseContent(
                msg='The file name and extension "'
                + addThreePeriods(file.name, 30)
                + '" already exist in the folder',
                data=None,
            ),
        )

    _bytes, prefix = get_sufix_to_bytes(byteSize)

    filedata = FileData(byteData=byteData)
    folder = folder_by_id(db, folderId)
    owner = user_by_id(db, owner_id)

    new_file = insert_file(db, name, extension, _bytes, prefix, folder, filedata, owner)

    return new_file


def download_serv(db, id, owner_id):
    data = download_file(db, id, owner_id)
    # byte_data = get_bytes_data()
    return [data, data.fileData.byteData]


def update_file_name_serv(
    db: Session, file_id: str, body: FileUpdate, owner_id: str
) -> DefaultDefReponse | bool:

    fullname = body.new_name + "." + body.extension

    exist = file_by_name_in_folder(db, fullname, body.folder_id, owner_id)

    if exist:
        return DefaultDefReponse(
            status=422,
            content=DefaultDefReponseContent(
                msg="Can't update the file \""
                + addThreePeriods(body.name, 30)
                + '" to "'
                + addThreePeriods(body.new_name, 30)
                + '" the name already exist in the folder',
                data=None,
            ),
        )

    file_update_name(db, fullname, body.new_name, file_id, owner_id, body.folder_id)

    return True
