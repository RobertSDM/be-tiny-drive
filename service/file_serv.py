import json
from pickle import TRUE
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.file_model import File
from database.schemas import DefaultDefReponse, DefaultDefReponseContent, FileUpdate
from controller.convert.convert_data import get_sufix_to_bytes
from database.repository.file_repository import (
    file_by_name_in_folder,
    file_update_name,
    insert_file as fs,
    download_file,
)
from utils.add_three_periods import addThreePeriods


def save_file_serv(
    db: Session, name, folderId, extension, byteData, byteSize, owner_id
) -> DefaultDefReponse | File:
    file = (
        db.query(File)
        .filter(
            and_(
                and_(
                    File.folder_id == folderId, File.fullname == name + "." + extension
                ),
                File.owner_id == owner_id,
            )
        )
        .first()
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
    new_file = fs(db, name, extension, byteData, _bytes, prefix, owner_id, folderId)

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
                + "\" to \""
                + addThreePeriods(body.new_name, 30)
                + "\" the name already exist in the folder",
                data=None,
            ),
        )

    file_update_name(db, fullname, body.new_name, file_id, owner_id)

    return True
