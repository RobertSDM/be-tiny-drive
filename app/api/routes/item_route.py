from typing import Annotated
from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.clients.sqlalchemy_client import db_client
from app.core.schemas import ListItemResponse, SingleItemResponse, SingleResponse
from app.enums.enums import ItemType
from app.service.item_serv import (
    delete_item_serv,
    all_items_in_folder_serv,
    all_root_items_serv,
    download_folder_serv,
    download_many_serv,
    download_serv,
    image_preview_serv,
    item_by_id_serv,
    item_save_folder_serv,
    item_save_item_serv,
    item_update_name,
    search_serv,
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


@item_router.get("/search/{ownerid}")
def item_search_route(
    ownerid: str,
    q: str,
    type: ItemType | None = None,
    db: Session = Depends(db_client.get_session),
):
    items = search_serv(db, ownerid, q, type)

    return JSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/{ownerid}/{id}")
def get_item_by_id_route(ownerid: str, id: str, db=Depends(db_client.get_session)):
    item = item_by_id_serv(db, ownerid, id)

    return JSONResponse(SingleItemResponse(data=item).model_dump())


class DownloadManyFilesBody(BaseModel):
    fileids: list[str]


@item_router.get("/download/many/{ownerid}")
def download_many_files_route(
    body: DownloadManyFilesBody,
    ownerid: str,
    db: Session = Depends(db_client.get_session),
):
    zip = download_many_serv(db, body.fileids, ownerid)

    return StreamingResponse(zip, media_type="application/zip")


@item_router.get("/download/folder/{ownerid}/{parentid}")
def donwload_folder_route(
    ownerid: str, parentid: str, db: Session = Depends(db_client.get_session)
):
    zip = download_folder_serv(db, ownerid, parentid)

    return StreamingResponse(
        zip,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename='downloaded_content'"},
    )


@item_router.get("/download/{ownerid}/{id}")
def download_file_route(id: str, ownerid: str, db=Depends(db_client.get_session)):

    print(id)
    url = download_serv(db, id, ownerid)

    return JSONResponse(SingleResponse(data=url).model_dump())


@item_router.get("/img/preview/{ownerid}/{id}")
def image_preview(ownerid: str, id: str, db: Session = Depends(db_client.get_session)):
    url = image_preview_serv(db, ownerid, id)

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
