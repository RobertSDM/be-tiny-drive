from database.models.FolderModel import Folder
from database.models.FileModel import File
from database.models.UserModel import User
from database.schemas.schemas import ResponseFolder, ResponseFile, ResponseUser


def convert_user_to_response_user(user: User | None) -> ResponseUser:
    if not user:
        return None

    return ResponseUser(id=str(user.id), user_name=user.user_name, email=user.email)


def convert_folder_to_response_folder_json(
    folder: Folder | None,
) -> dict | None:
    if not folder:
        return None

    folderC_id = str(folder.folderC_id) if folder.folderC_id else None

    return {
        "id": str(folder.id),
        "name": folder.name,
        "folder": convert_folder_to_response_folder_json(folder.folder),
        "folderC_id": folderC_id,
        "tray": folder.tray,
    }


def convert_folder_to_response_folder(folder: Folder | None) -> ResponseFolder | None:
    if not folder:
        return None

    folderC_id = str(folder.folderC_id) if folder.folderC_id else None

    return ResponseFolder(
        id=str(folder.id),
        name=folder.name,
        folder=convert_folder_to_response_folder(folder.folder),
        folderC_id=folderC_id,
    )


def convert_file_to_response_file_json(file: File) -> ResponseFile:
    if not file:
        return None
    
    return {
        "id": str(file.id),
        "name": file.name,
        "byteSize": file.byteSize,
        "folder": convert_folder_to_response_folder_json(file.folder),
        "folder_id": str(file.folder_id),
        "fullname": file.fullname,
        "prefix": file.prefix,
        "extension": file.extension,
    }


def convert_file_to_response_file(file: File) -> ResponseFile:
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

    for i in content["files"]:
        files.append(convert_file_to_response_file_json(i))

    folders = []

    for i in content["folders"]:
        folders.append(convert_folder_to_response_folder_json(i))

    resquestedFolder = {}

    if content.get("requestedFolder", None):
        resquestedFolder = convert_folder_to_response_folder_json(
            content["requestedFolder"]
        )

    return {"files": files, "folders": folders, "requestedFolder": resquestedFolder}
