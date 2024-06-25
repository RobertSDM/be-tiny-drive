from database.models.FolderModel import Folder
from database.models.FileModel import File
from database.schemas.schemas import ResponseFolder, ResponseFile

def convert_folder_to_response_folder(folder: Folder | None) -> ResponseFolder | None:
    if(not folder):
        return None

    folderC_id = str(folder.folderC_id) if folder.folderC_id else None

    print(folderC_id)

    return ResponseFolder(
        id=str(folder.id),
        name=folder.name,
        folder=convert_folder_to_response_folder(folder.folder),
        folderC_id=folderC_id
    )

def convert_file_to_response_file(file: File) -> ResponseFile:
    return ResponseFile(
        id=str(file.id),
        name=file.name,
        byteSize=file.byteSize,
        folder=convert_folder_to_response_folder(file.folder),
        folder_id=str(file.folder_id),
        fullname=file.fullname,
        prefix=file.prefix,
        extension=file.extension
    )