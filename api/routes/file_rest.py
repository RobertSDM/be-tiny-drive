import json
from os import name
from typing import Annotated
from fastapi import APIRouter, File, Form, Request, Response, Depends, UploadFile
from pydantic import BaseModel
from service.file_serv import save_file_serv, download_serv, update_file_name_serv
from database.repositories.file_repository import (
    delete_file,
)
from schemas.schemas import DefaultDefReponse, FileBody, FileUpdate
from database.db_engine import get_session
from utils import (
    convert_file_to_response_file,
)

file_router = APIRouter()


@file_router.post("/save", status_code=200)
def __save_file_route(
    file: Annotated[bytes, File()],
    name: Annotated[str, Form()],
    extension: Annotated[str, Form()],
    size: Annotated[int, Form()],
    ownerid: Annotated[str, Form()],
    folderid: Annotated[str, Form()],
    db=Depends(get_session),
):
    res = save_file_serv(
        db,
        name,
        folderid,
        extension,
        file,
        size,
        ownerid,
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
