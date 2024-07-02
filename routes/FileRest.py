import json
from fastapi import APIRouter, Response, Depends
from service.file_serv import save_file, download_service
from database.repository.FileRepository import (
    files_with_no_parent,
    find_all_files,
    files_by_folder,
    delete_file,
)
from database.schemas.schemas import DefaultDefReponse, FileBody
from fastapi.responses import StreamingResponse
from database.init_database import get_session
from controller.convert_data import (
    convert_content_to_json,
    convert_file_to_response_file,
    convert_file_to_response_file_json,
    convert_folder_to_response_folder_json,
)

route = APIRouter()


@route.get("/get_root_content/{owner_id}")
def get_root_files(owner_id: str, db=Depends(get_session)):
    content = files_with_no_parent(db, owner_id)

    conv_content = convert_content_to_json(content)

    if len(content) > 0:
        return Response(
            status_code=200, content=json.dumps({"msg": None, "data": conv_content})
        )
    else:
        return Response(
            status_code=204, content=json.dumps({"msg": None, "data": None})
        )


@route.post("/save/file", status_code=200)
def save_file_route(file: FileBody, db=Depends(get_session)):
    res = save_file(
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
                    "data": convert_file_to_response_file_json(res.content.data),
                }
            ),
            status_code=res.status,
        )
    elif res:
        return Response(
            json.dumps({"msg": None, "data": convert_file_to_response_file_json(res)}),
            status_code=200,
        )
    else:
        return Response(
            status_code=500,
            content=json.dumps({"msg": "Error to save the " + file.name}),
        )


@route.get("/find/all")
def find_all(db=Depends(get_session)):
    return find_all_files(db)


@route.get("/download/{id}")
def download(id: str, db=Depends(get_session)):
    data, formated_byte_data = download_service(db, id)

    return StreamingResponse(
        formated_byte_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={data['fullname']}"},
    )


@route.get("/from/folder/{id}/{owner_id}", status_code=200)
def findByFolder(id: str, owner_id: str, db=Depends(get_session)):
    content = files_by_folder(db, id, owner_id)

    conv_content = convert_content_to_json(content)

    if len(content) > 0:
        return Response(
            status_code=200, content=json.dumps({"msg": None, "data": conv_content})
        )
    else:
        return Response(status_code=204)


@route.delete("/file/delete/{id}/{owner_id}", status_code=200)
def deleteById(id: str, owner_id: str, db=Depends(get_session)):
    deleted_file = delete_file(db, id, owner_id)

    if deleted_file:
        return convert_file_to_response_file(deleted_file)
    else:
        Response(status_code=500)
