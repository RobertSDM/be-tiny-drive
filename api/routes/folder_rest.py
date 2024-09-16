import json
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, Response
from database.schemas import DefaultDefReponse, FolderBody, FolderUpdate
from database.repository.folder_repository import (
    delete_folder,
)
from database.init_database import get_session
from controller.convert.convert_types import (
    convert_folder_to_response_folder,
)
from service.folder_serv import download_zip_serv, save_folder_serv, update_folder_name_serv

folder_router = APIRouter()


@folder_router.get("/download/zip/{id}/{owner_id}", status_code=200)
def __download_folder_zip(id: str, owner_id: str, db=Depends(get_session)):

    data = download_zip_serv(db, id, owner_id)

    return StreamingResponse(
        data,
        media_type="application/zip",
        status_code=200,
        headers={
            "Content-Disposition": f"inline;",
            "Content-Length": str(data.getbuffer().nbytes),
        },
    )


@folder_router.post("/save", status_code=200)
def __save_folder_route(folder: FolderBody, db=Depends(get_session)):
    res = save_folder_serv(db, folder.name, folder.parentId, folder.owner_id)

    if isinstance(res, DefaultDefReponse):
        return Response(
            json.dumps(
                {
                    "msg": res.content.msg,
                    "data": convert_folder_to_response_folder(res.content.data, True),
                }
            ),
            status_code=res.status,
        )
    elif res:
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


@folder_router.put("/update/name/{id}/{owner_id}", status_code=200)
def __update_folder_name(
    id: str, body: FolderUpdate, owner_id: str, db=Depends(get_session)
):
    res = update_folder_name_serv(db, id, body, owner_id)

    if isinstance(res, DefaultDefReponse):
        return Response(
            json.dumps(
                {
                    "msg": res.content.msg,
                    "data": convert_folder_to_response_folder(res.content.data, True),
                }
            ),
            status_code=res.status,
        )
    elif res:
        return Response(
            json.dumps(
                {
                    "msg": None,
                    "data": {"tray": res},
                }
            ),
            status_code=200,
        )
    else:
        return Response(
            status_code=500,
            content=json.dumps({"msg": "Error to update the name"}),
        )


@folder_router.delete("/delete/{id}/{owner_id}", status_code=200)
def __delete_folder_by_id(id: str, owner_id: str, db=Depends(get_session)):
    deleted_folder = delete_folder(db, id, owner_id)

    if deleted_folder:
        return convert_folder_to_response_folder(deleted_folder, True)
    else:
        Response(status_code=500)
