from fastapi import APIRouter, Depends, Response
from database.schemas.schemas import FolderBody
from database.repository.FolderRepository import save_folder
from database.init_database import get_session
import json

folder_router = APIRouter()

@folder_router.post("/save/folder", status_code=200)
def save_folder_route(folder: FolderBody, db = Depends(get_session)):
    print(folder.parentId)
    new_folder = save_folder(db, folder.name, folder.parentId)

    if(new_folder):
        return new_folder
    else:
        return Response(status_code=500)
