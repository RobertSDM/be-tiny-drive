import json
from fastapi import APIRouter, Depends, Response
from database.schemas.schemas import DefaultDefReponse, FolderBody
from database.repository.FolderRepository import save_folder, delete_folder
from database.init_database import get_session
from controller.convert_data import (
    convert_folder_to_response_folder,
    convert_folder_to_response_folder_json,
)

folder_router = APIRouter()


@folder_router.post("/save/folder", status_code=200)
def save_folder_route(folder: FolderBody, db=Depends(get_session)):
    res = save_folder(db, folder.name, folder.parentId, folder.owner_id)


    if res:
        print(res.name)
        return Response(
            json.dumps(
                {"msg": None, "data": convert_folder_to_response_folder_json(res)}
            ),
            status_code=200,
        )
    else:
        return Response(
            status_code=500,
            content=json.dumps({"msg": "Error to save the " + folder.name}),
        )


@folder_router.delete("/folder/delete/{id}/{owner_id}", status_code=200)
def deleteById(id: str, owner_id: str, db=Depends(get_session)):
    deleted_folder = delete_folder(db, id, owner_id)

    if deleted_folder:
        return convert_folder_to_response_folder_json(deleted_folder)
    else:
        Response(status_code=500)
