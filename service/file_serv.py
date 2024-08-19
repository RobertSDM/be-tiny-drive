from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.file_model import File
from database.schemas import DefaultDefReponse, DefaultDefReponseContent
from controller.convert.convert_data import get_sufix_to_bytes
from database.repository.file_repository import insert_file as fs, download_file
from controller.convert.convert_data import get_bytes_data
import io

from utils.addThreePeriods import addThreePeriods


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
                msg="The file name and extension \""
                + addThreePeriods(file.name, 30)
                + "\" already exist in the folder",
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
