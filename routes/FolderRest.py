from fastapi import APIRouter, Depends, Response
from database.schemas.schemas import FolderBody, FolderSchema
from database.repository.FolderRepository import save_folder
from database.init_database import get_session
import json

folder_router = APIRouter()

@folder_router.post("/save/folder", status_code=200)
def save_folder_route(folder: FolderBody, db = Depends(get_session)):
    new_folder = save_folder(db, folder.name, folder.parentId)

    if(new_folder):
        return FolderSchema(
            id=new_folder.id,
            files=new_folder.files,
            folder=new_folder.folder,
            folderC_id=new_folder.folderC_id,
            name=new_folder.name,
            folders=new_folder.folders
        )
    else:
        return Response(status_code=500)
