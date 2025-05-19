from typing import Annotated
from fastapi import APIRouter, Depends, Form, Response, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.clients.sqlalchemy_client import db_client
from app.core.schemas import ListItemResponse, SingleItemResponse, SingleResponse
from app.service.item_serv import (
    delete_item_serv,
    all_items_in_folder_serv,
    all_root_items_serv,
    download_serv,
    item_by_id_serv,
    item_save_folder_serv,
    item_save_item_serv,
    item_update_name,
)


item_router = APIRouter()


@item_router.post("/save", status_code=200)
def save_file_route(
    file: UploadFile,
    ownerid: Annotated[str, Form()],
    parentid: Annotated[str | None, Form()] = None,
    db=Depends(db_client.get_session),
):
    item = item_save_item_serv(db, file, ownerid, parentid)

    return JSONResponse(SingleItemResponse(data=item).model_dump())


class SaveFolderBody(BaseModel):
    name: str
    parentid: str | None
    ownerid: str


@item_router.post("/save/folder")
def save_folder_route(body: SaveFolderBody, db=Depends(db_client.get_session)):
    folder = item_save_folder_serv(db, body.ownerid, body.name, body.parentid)

    return JSONResponse(SingleItemResponse(data=folder).model_dump())


@item_router.get("/all/{ownerid}")
def get_all_items_route(ownerid: str, db=Depends(db_client.get_session)):
    items = all_root_items_serv(db, ownerid)

    return JSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/all/{ownerid}/{parentid}")
def get_all_item_in_folder_route(
    ownerid: str, parentid: str, db=Depends(db_client.get_session)
):
    items = all_items_in_folder_serv(db, ownerid, parentid)

    return JSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/{ownerid}/{id}")
def get_item_by_id_route(ownerid: str, id: str, db=Depends(db_client.get_session)):
    item = item_by_id_serv(db, ownerid, id)

    return JSONResponse(SingleItemResponse(data=item).model_dump())


@item_router.get("/download/{ownerid}/{id}")
def download_file_route(id: str, ownerid: str, db=Depends(db_client.get_session)):
    url = download_serv(db, id, ownerid)

    return JSONResponse(SingleResponse(data=url).model_dump())


class UpdateNameBody(BaseModel):
    name: str


@item_router.put("/update/{ownerid}/{id}/name")
def put_name_route(
    id: str, ownerid: str, body: UpdateNameBody, db=Depends(db_client.get_session)
):
    item = item_update_name(db, id, ownerid, body.name)

    return JSONResponse(SingleItemResponse(data=item).model_dump())


@item_router.delete("/delete/{ownerid}/{id}")
def delete_item_by_id_route(ownerid: str, id: str, db=Depends(db_client.get_session)):
    item = delete_item_serv(db, ownerid, id)

    return JSONResponse(SingleItemResponse(data=item).model_dump())
