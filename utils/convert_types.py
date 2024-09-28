import json
from database.model.folder_model import Folder
from database.model.file_model import File
from database.model.user_model import User
from database.schemas import ResponseFile, ResponseFolderBase, ResponseUser


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
    folder: Folder | None, to_json: bool = False
) -> dict | None:
    if not folder:
        return None

    folderC_id = str(folder.folderC_id) if folder.folderC_id else None

    if to_json:
        return {
            "id": str(folder.id),
            "name": folder.name,
            "folderC_id": folderC_id,
            "tray": folder.tray,
        }
    else:
        return ResponseFolderBase(
            id=str(folder.id),
            name=folder.name,
            folderC_id=folderC_id,
        )


def convert_file_to_response_file(file: File, to_json: bool = False) -> ResponseFile:
    if not file:
        return None

    if to_json:
        try:
            return {
                "id": str(file.id),
                "name": file.name,
                "byteSize": file.byteSize,
                "folder_id": str(file.folder_id),
                "fullname": file.fullname,
                "prefix": file.prefix,
                "extension": file.extension,
            }
        except Exception as e:
            return {
                "id": str(file.id),
                "name": file.name,
                "byteSize": file.byteSize,
                "folder_id": (str(file.folderC_id)),
                "fullname": file.fullname,
                "prefix": file.prefix,
                "extension": file.extension,
            }
    else:
        try:

            return ResponseFile(
                id=str(file.id),
                name=file.name,
                byteSize=file.byteSize,
                folder_id=str(file.folderC_id),
                fullname=file.fullname,
                prefix=file.prefix,
                extension=file.extension,
            )
        except Exception as e:
            return ResponseFile(
                id=str(file.id),
                name=file.name,
                byteSize=file.byteSize,
                folder_id=(str(file.folder_id)),
                fullname=file.fullname,
                prefix=file.prefix,
                extension=file.extension,
            )


def convert_content_to_json(content: list[Folder | File], requestedFolder=None):
    resquestedFolder = {}
    content_json = []

    for i in content:
        if i.type == "FILE":
            content_json.append(convert_file_to_response_file(i, True))
        else:
            content_json.append(convert_folder_to_response_folder(i, True))

    if requestedFolder:
        resquestedFolder = convert_folder_to_response_folder(requestedFolder, True)

    return {"content": content_json, "requestedFolder": resquestedFolder}
