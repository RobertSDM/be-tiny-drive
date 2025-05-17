from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.clients.sqlalchemy_client import db_client
from app.core.schemas import ListItemResponse, SingleItemResponse
from app.enums.enums import ItemType
from app.service.item_serv import (
    delete_item_serv,
    all_items_in_folder_serv,
    all_root_items_serv,
    item_by_id_serv,
    item_create_serv,
    item_update_name,
)


item_router = APIRouter()


class SaveRequest(BaseModel):
    # file: Annotated[bytes, File()]
    name: Annotated[str, Form()]
    extension: Annotated[str, Form()]
    path: Annotated[str, Form()]
    size: Annotated[int, Form()]
    ownerid: Annotated[str, Form()]
    type: Annotated[ItemType, Form()]
    parentid: Annotated[Optional[str], Form()]


@item_router.post("/save", status_code=200)
def save_file_route(
    request: SaveRequest,
    db=Depends(db_client.get_session),
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
def all_items(ownerid: str, db=Depends(db_client.get_session)):
    items = all_root_items_serv(db, ownerid)

    return JSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/all/{ownerid}/{parentid}")
def all_item_in_folder(ownerid: str, parentid: str, db=Depends(db_client.get_session)):
    items = all_items_in_folder_serv(db, ownerid, parentid)

    return JSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/{ownerid}/{id}")
def item_by_id(ownerid: str, id: str, db=Depends(db_client.get_session)):
    item = item_by_id_serv(db, ownerid, id)

    return JSONResponse(SingleItemResponse(data=item).model_dump())


# @item_router.get("/download/{id}/{owner_id}")
# def __download_file(id: str, owner_id: str, db=Depends(db_client.get_session)):
#     data, formated_byte_data = download_serv(db, id, owner_id)

#     return {"data": formated_byte_data, "name": data.fullname}


class UpdateNameBody(BaseModel):
    name: str


@item_router.put("/update/{id}/name")
def update_name(id: str, body: UpdateNameBody, db=Depends(db_client.get_session)):
    item = item_update_name(db, id, body.name)

    return JSONResponse(SingleItemResponse(data=item).model_dump())


@item_router.delete("/delete/{ownerid}/{id}")
def delete_file_by_id(ownerid: str, id: str, db=Depends(db_client.get_session)):
    item = delete_item_serv(db, ownerid, id)

    return JSONResponse(SingleItemResponse(data=item).model_dump())
