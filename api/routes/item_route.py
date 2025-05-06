from typing import Annotated, Optional
from fastapi import APIRouter, Depends, File, Form, Response
from pydantic import BaseModel

from database.db_engine import get_session
from service.item_serv import get_all_root_items, item_create_serv


item_router = APIRouter()


class SaveRequest(BaseModel):
    # file: Annotated[bytes, File()]
    name: Annotated[str, Form()]
    extension: Annotated[str, Form()]
    path: Annotated[str, Form()]
    size: Annotated[int, Form()]
    ownerid: Annotated[int, Form()]
    folderid: Optional[Annotated[int, Form()]]


@item_router.post("/save", status_code=200)
def save_file_route(
    request: SaveRequest,
    db=Depends(get_session),
):
    item = item_create_serv(
        db,
        request.name,
        request.folderid,
        request.extension,
        request.size,
        bytes(),
        request.ownerid,
        request.path,
    )

    if not item:
        return Response(status_code=409)

    return item


@item_router.get("/root/all/{ownerid}")
def all_items(ownerid: int, db=Depends(get_session)):
    items = get_all_root_items(db, ownerid)

    return items


# @item_router.get("/download/{id}/{owner_id}")
# def __download_file(id: str, owner_id: str, db=Depends(get_session)):
#     data, formated_byte_data = download_serv(db, id, owner_id)

#     return {"data": formated_byte_data, "name": data.fullname}


# @item_router.put("/update/name/{id}/{owner_id}", status_code=200)
# def __update_file_name(
#     id: str, body: FileUpdate, owner_id: str, db=Depends(get_session)
# ):
#     res = update_file_name_serv(db, id, body, owner_id)

#     if isinstance(res, DefaultDefReponse):
#         return Response(
#             json.dumps(
#                 {
#                     "msg": res.content.msg,
#                     "data": convert_file_to_response_file(res.content.data, True),
#                 }
#             ),
#             status_code=res.status,
#         )
#     elif res:
#         return Response(
#             status_code=200,
#         )
#     else:
#         return Response(
#             status_code=500,
#             content=json.dumps({"msg": "Error to update the name"}),
#         )


# @item_router.delete("/delete/{id}/{owner_id}", status_code=200)
# def __delete_file_by_id(id: str, owner_id: str, db=Depends(get_session)):
#     deleted_file = delete_file(db, id, owner_id)

#     if deleted_file:
#         return convert_file_to_response_file(deleted_file)
#     else:
#         Response(status_code=500)
