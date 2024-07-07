import json
from fastapi import APIRouter, Response, Depends
from service.file_serv import save_file_serv, download_serv
from database.repository.file_repository import (
    delete_file,
)
from database.schemas import DefaultDefReponse, FileBody
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


@file_router.get("/download/{id}")
def __download_file(id: str, db=Depends(get_session)):
    data, formated_byte_data = download_serv(db, id)

    return StreamingResponse(
        formated_byte_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={data.file.fullname}"},
    )


@file_router.delete("/delete/{id}/{owner_id}", status_code=200)
def __delete_file_by_id(id: str, owner_id: str, db=Depends(get_session)):
    deleted_file = delete_file(db, id, owner_id)

    if deleted_file:
        return convert_file_to_response_file(deleted_file)
    else:
        Response(status_code=500)
