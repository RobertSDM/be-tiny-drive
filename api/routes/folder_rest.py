import json
from fastapi import APIRouter, Depends, Response
from database.schemas import FolderBody
from database.repository.folder_repository import insert_folder, delete_folder
from database.init_database import get_session
from controller.convert.convert_types import (
    convert_folder_to_response_folder,
)

folder_router = APIRouter()


@folder_router.post("/save", status_code=200)
def __save_folder_route(folder: FolderBody, db=Depends(get_session)):
    res = insert_folder(db, folder.name, folder.parentId, folder.owner_id)

    if res:
        return Response(
            json.dumps(
                {"msg": None, "data": convert_folder_to_response_folder(res, True)},
            ),
            status_code=200,
        )
    else:
        return Response(
            status_code=500,
            content=json.dumps({"msg": "Error to save the " + folder.name}),
        )


@folder_router.delete("/delete/{id}/{owner_id}", status_code=200)
def __delete_folder_by_id(id: str, owner_id: str, db=Depends(get_session)):
    deleted_folder = delete_folder(db, id, owner_id)

    if deleted_folder:
        return convert_folder_to_response_folder(deleted_folder, True)
    else:
        Response(status_code=500)
