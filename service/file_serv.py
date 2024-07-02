from sqlalchemy import and_
from sqlalchemy.orm import Session
from controller.convert_data import convert_file_to_response_file_json, convert_folder_to_response_folder_json
from database.models.FileModel import File
from database.repository.UserRepository import find_user_by_id
from database.schemas.schemas import DefaultDefReponse, DefaultDefReponseContent
from service.convert_data import get_sufix_to_bytes
from database.repository.FileRepository import files_with_no_parent, save_file as fs, find_by_file_id_download
from service.convert_data import get_bytes_data
import io


def save_file(
    db: Session, name, folderId, extension, byteData, byteSize, owner_id
) -> DefaultDefReponse | File:
    file = (
        db.query(File)
        .filter(and_(File.folder_id == folderId, File.fullname == name + "." + extension))
        .first()
    )

    if file:
        return DefaultDefReponse(
            status=422,
            content=DefaultDefReponseContent(
                msg="The user name and extension 'name.extension' already exist in the folder",
                data=None,
            ),
        )

    _bytes, prefix = get_sufix_to_bytes(byteSize)
    new_file = fs(db, name, extension, byteData, _bytes, prefix, owner_id, folderId)

    return new_file


def download_service(db, id):
    data = find_by_file_id_download(db, id)
    byte_data = get_bytes_data(data["byteData"])
    formated_byte_data = io.BytesIO(byte_data)
    return [data, formated_byte_data]


