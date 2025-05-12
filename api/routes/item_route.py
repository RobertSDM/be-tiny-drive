from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Form, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.schemas import ListItemResponse, SingleItemResponse
from database.db_engine import get_session
from database.models.enums.content_type import ItemType
from service.item_serv import (
    delete_item_serv,
    get_all_items_in_folder,
    get_all_root_items_serv,
    item_create_serv,
)


item_router = APIRouter()


class SaveRequest(BaseModel):
    # file: Annotated[bytes, File()]
    name: Annotated[str, Form()]
    extension: Annotated[str, Form()]
    path: Annotated[str, Form()]
    size: Annotated[int, Form()]
    ownerid: Annotated[int, Form()]
    type: Annotated[ItemType, Form()]
    parentid: Annotated[Optional[int], Form()]


@item_router.post("/save", status_code=200)
def save_file_route(
    request: SaveRequest,
    db=Depends(get_session),
):
    item = item_create_serv(
        db,
        request.name,
        request.parentid,
        request.extension,
        request.size,
        bytes(),
        request.ownerid,
        request.path,
        request.type,
    )

    return JSONResponse(SingleItemResponse(data=item).model_dump())


@item_router.get("/all/{ownerid}")
def all_items(ownerid: int, db=Depends(get_session)):
    items = get_all_root_items_serv(db, ownerid)

    return JSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/all/{ownerid}/{parentid}")
def all_item_in_folder(ownerid: int, parentid: int, db=Depends(get_session)):
    items = get_all_items_in_folder(db, ownerid, parentid)

    return JSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


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


@item_router.delete("/delete/{ownerid}/{id}")
def delete_file_by_id(ownerid: str, id: str, db=Depends(get_session)):
    item = delete_item_serv(db, ownerid, id)

    return JSONResponse(SingleItemResponse(data=item).model_dump())
