from database.models.folder_model import Folder
from database.models.file_model import File
from database.models.user_model import User
from database.schemas import ResponseFolder, ResponseFile, ResponseUser


def convert_user_to_response_user(
    user: User | None, json: bool = False
) -> ResponseUser:
    if not user:
        return None

    if json:
        return {"id": str(user.id), "user_name": user.user_name, "email": user.email}
    else:
        return ResponseUser(id=str(user.id), user_name=user.user_name, email=user.email)


def convert_folder_to_response_folder(
    folder: Folder | None, json: bool = False
) -> dict | None:
    if not folder:
        return None

    folderC_id = str(folder.folderC_id) if folder.folderC_id else None

    if json:
        return {
            "id": str(folder.id),
            "name": folder.name,
            "folder": convert_folder_to_response_folder(folder.folder, json),
            "folderC_id": folderC_id,
            "tray": folder.tray,
        }
    else:
        return ResponseFolder(
            id=str(folder.id),
            name=folder.name,
            folder=convert_folder_to_response_folder(folder.folder),
            folderC_id=folderC_id,
        )


def convert_file_to_response_file(file: File, json: bool = False) -> ResponseFile:
    if not file:
        return None

    if json:
        return {
            "id": str(file.id),
            "name": file.name,
            "byteSize": file.byteSize,
            "folder": convert_folder_to_response_folder(file.folder, json),
            "folder_id": str(file.folder_id),
            "fullname": file.fullname,
            "prefix": file.prefix,
            "extension": file.extension,
        }
    else:
        return ResponseFile(
            id=str(file.id),
            name=file.name,
            byteSize=file.byteSize,
            folder=convert_folder_to_response_folder(file.folder),
            folder_id=str(file.folder_id),
            fullname=file.fullname,
            prefix=file.prefix,
            extension=file.extension,
        )


def convert_content_to_json(content):
    files = []
    folders = []
    resquestedFolder = {}

    for i in content["files"]:
        files.append(convert_file_to_response_file(i, True))

    for i in content["folders"]:
        folders.append(convert_folder_to_response_folder(i, True))

    if content.get("requestedFolder", None):
        resquestedFolder = convert_folder_to_response_folder(
            content["requestedFolder"], True
        )

    return {"files": files, "folders": folders, "requestedFolder": resquestedFolder}
