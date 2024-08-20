import json
from os import name
from fastapi import APIRouter, Response, Depends
from service.file_serv import save_file_serv, download_serv, update_file_name_serv
from database.repository.file_repository import (
    delete_file,
)
from database.schemas import DefaultDefReponse, FileBody, FileUpdate
from fastapi.responses import StreamingResponse
from database.init_database import get_session
from controller.convert.convert_types import (
    convert_file_to_response_file,
)

file_router = APIRouter()


@file_router.post("/save", status_code=200)
def __save_file_route(file: FileBody, db=Depends(get_session)):
    res = save_file_serv(
        db,
        file.name,
        file.folderId,
        file.extension,
        file.byteData,
        file.byteSize,
        file.owner_id,
    )

    if isinstance(res, DefaultDefReponse):
        return Response(
            json.dumps(
                {
                    "msg": res.content.msg,
                    "data": convert_file_to_response_file(res.content.data, True),
                }
            ),
            status_code=res.status,
        )
    elif res:
        return Response(
            json.dumps({"msg": None, "data": convert_file_to_response_file(res, True)}),
            status_code=200,
        )
    else:
        return Response(
            status_code=500,
            content=json.dumps({"msg": "Error to save the " + file.name}),
        )


## Not beeing used
# @file_router.get("/find/all")
# def __find_all(db=Depends(get_session)):
#     return find_all_files(db)


@file_router.get("/download/{id}/{owner_id}")
def __download_file(id: str, owner_id: str, db=Depends(get_session)):
    data, formated_byte_data = download_serv(db, id, owner_id)

    return {"data": formated_byte_data, "name": data.fullname}


@file_router.put("/update/name/{id}/{owner_id}", status_code=200)
def __update_file_name(
    id: str, body: FileUpdate, owner_id: str, db=Depends(get_session)
):
    res = update_file_name_serv(db, id, body, owner_id)

    if isinstance(res, DefaultDefReponse):
        return Response(
            json.dumps(
                {
                    "msg": res.content.msg,
                    "data": convert_file_to_response_file(res.content.data, True),
                }
            ),
            status_code=res.status,
        )
    elif res:
        return Response(
            status_code=200,
        )
    else:
        return Response(
            status_code=500,
            content=json.dumps({"msg": "Error to update the name"}),
        )


@file_router.delete("/delete/{id}/{owner_id}", status_code=200)
def __delete_file_by_id(id: str, owner_id: str, db=Depends(get_session)):
    deleted_file = delete_file(db, id, owner_id)

    if deleted_file:
        return convert_file_to_response_file(deleted_file)
    else:
        Response(status_code=500)
