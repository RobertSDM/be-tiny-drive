from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, Form, UploadFile
from fastapi.responses import ORJSONResponse, StreamingResponse
from pydantic import BaseModel
from pytest import Session

from app.core.schemas import FileResponseStructure
from app.lib.sqlalchemy import client
from app.core.schemas import FileType, Sort, SortOrder
from app.features.file.services import (
    item_create_serv,
    item_delete_serv,
    item_read_serv,
    item_update_serv,
)
from app.middlewares.authorization_middleware import authorization_middleware


item_router = APIRouter(dependencies=[Depends(authorization_middleware)])


@item_router.post("/")
def save_file_route(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    ownerid: Annotated[str, Form()],
    parentid: Annotated[str | None, Form()] = None,
    db=Depends(client.get_session),
):
    item = item_create_serv.item_save_item_serv(db, file, ownerid, parentid)
    if item.type == FileType.FILE:
        background_tasks.add_task(
            item_create_serv.item_create_preview_serv, db, ownerid, item.id
        )

    return ORJSONResponse(FileResponseStructure(data=item).model_dump())


@item_router.get("/{ownerid}")
def get_all_items_route(
    ownerid: str,
    p: int = 0,
    order: SortOrder = SortOrder.ASC,
    sort: Sort = Sort.NAME,
    db=Depends(client.get_session),
):
    items = item_read_serv.all_root_items_serv(db, ownerid, p, order, sort)

    return ORJSONResponse(
        FileResponseStructure(data=items, count=len(items)).model_dump()
    )


@item_router.get("/{parentid}/account/{ownerid}")
def get_all_item_in_folder_route(
    ownerid: str,
    parentid: str,
    p: int = 0,
    order: SortOrder = SortOrder.ASC,
    sort: Sort = Sort.NAME,
    db=Depends(client.get_session),
):
    items = item_read_serv.all_items_in_folder_serv(
        db, ownerid, parentid, p, order, sort
    )

    return ORJSONResponse(
        FileResponseStructure(data=items, count=len(items)).model_dump()
    )


@item_router.get("/{ownerid}/search")
def item_search_route(
    ownerid: str,
    q: str,
    type: FileType | None = None,
    db: Session = Depends(client.get_session),
):
    items = item_read_serv.search_serv(db, ownerid, q, type)

    return ORJSONResponse(
        FileResponseStructure(data=items, count=len(items)).model_dump()
    )


@item_router.get("/{id}/account/{ownerid}")
def get_item_by_id_route(ownerid: str, id: str, db=Depends(client.get_session)):
    item = item_read_serv.item_by_id_serv(db, ownerid, id)

    return ORJSONResponse(FileResponseStructure(data=item).model_dump())


class DownloadManyFilesBody(BaseModel):
    fileids: list[str]


@item_router.get("/{ownerid}/download")
def download_many_files_route(
    body: DownloadManyFilesBody,
    ownerid: str,
    db: Session = Depends(client.get_session),
):
    zip = item_read_serv.download_many_serv(db, body.fileids, ownerid)

    return StreamingResponse(zip, media_type="application/zip")


@item_router.get("/{parentid}/account/{ownerid}/download")
def donwload_folder_route(
    ownerid: str, parentid: str, db: Session = Depends(client.get_session)
):
    zip = item_read_serv.download_folder_serv(db, ownerid, parentid)

    return StreamingResponse(
        zip,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="downloaded_content"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@item_router.get("/{id}/account/{ownerid}/download")
def download_file_route(id: str, ownerid: str, db=Depends(client.get_session)):
    data, content_type, filename = item_read_serv.download_serv(db, id, ownerid)

    return StreamingResponse(
        data,
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@item_router.get("/{id}/account/{ownerid}/preview")
def image_preview(ownerid: str, id: str, db: Session = Depends(client.get_session)):
    url = item_read_serv.preview_serv(db, ownerid, id)

    return ORJSONResponse(
        FileResponseStructure(data=url).model_dump(),
        headers={
            "Cache-Control": "max-age=3600, private",
        },
    )


class UpdateNameBody(BaseModel):
    name: str


@item_router.put("/{id}/account/{ownerid}/name")
def put_name_route(
    id: str, ownerid: str, body: UpdateNameBody, db=Depends(client.get_session)
):
    item = item_update_serv.item_update_name(db, id, ownerid, body.name)

    return ORJSONResponse(FileResponseStructure(data=item).model_dump())


class DeleteItemBody(BaseModel):
    itemids: list[str]


@item_router.delete("/{ownerid}")
def delete_item_route(
    ownerid: str, body: DeleteItemBody, db=Depends(client.get_session)
):
    deleted = item_delete_serv.delete_items_serv(db, ownerid, body.itemids)
    return ORJSONResponse(FileResponseStructure(data=deleted)).model_dump()


@item_router.get("/{id}/account}/{ownerid}/breadcrumb")
def breadcrumb_route(id: str, ownerid: str, db=Depends(client.get_session)):
    breadcrumb = item_read_serv.breadcrumb_serv(db, ownerid, id)

    return ORJSONResponse(
        FileResponseStructure(data=breadcrumb, count=len(breadcrumb)).model_dump()
    )
