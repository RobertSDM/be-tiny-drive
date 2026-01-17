from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Query, UploadFile
from fastapi.responses import ORJSONResponse, StreamingResponse, Response
from pydantic import BaseModel
from pytest import Session

from app.core.schemas import FileResponseStructure
from app.lib.sqlalchemy import client
from app.core.schemas import FileType, SortColumn, SortOrder
from app.features.file.services import (
    FileDeleteService,
    FileReadService,
    FileUpdateService,
    FileWriteService,
)
from app.middlewares.authorization_middleware import authorization_middleware


file_router = APIRouter(dependencies=[Depends(authorization_middleware)])


class SaveFolder(BaseModel):
    name: str


# Keep the declaration of this route before the route to save a file
@file_router.post("/account/{ownerid}/parent/folder")
@file_router.post("/account/{ownerid}/parent/{parentid}/folder")
def save_folder_route(
    ownerid: str,
    body: SaveFolder,
    parentid: Optional[str] = None,
    db=Depends(client.get_session),
    file_service: FileWriteService = Depends(FileWriteService),
):
    file = file_service.save_folder(db, ownerid, parentid, body.name)

    return ORJSONResponse(FileResponseStructure(files=[file]).model_dump())


@file_router.post("/account/{ownerid}/parent")
@file_router.post("/account/{ownerid}/parent/{parentid}")
def save_file_route(
    filedata: UploadFile,
    ownerid: str,
    background_tasks: BackgroundTasks,
    parentid: Optional[str] = None,
    db=Depends(client.get_session),
    file_service: FileWriteService = Depends(FileWriteService),
):
    file = file_service.save_file(db, filedata, ownerid, parentid)

    if file.type == FileType.FILE:
        background_tasks.add_task(lambda: file_service.create_preview(ownerid, file))

    return ORJSONResponse(FileResponseStructure(files=[file]).model_dump())


@file_router.get("/account/{ownerid}/parent")
@file_router.get("/account/{ownerid}/parent/{parentid}")
def get_files_route(
    ownerid: str,
    parentid: Optional[str] = None,
    p: int = 0,
    order: SortOrder = SortOrder.ASC,
    sort: SortColumn = SortColumn.NAME,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    items = file_service.get_files_in_folder(db, ownerid, parentid, p, order, sort)
    return ORJSONResponse(FileResponseStructure(files=items).model_dump())


@file_router.get("/account/{ownerid}/search")
def item_search_route(
    ownerid: str,
    q: str,
    type_: Optional[FileType] = Query(alias="type", default=None),
    db: Session = Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    items = file_service.search(db, ownerid, q, type_)

    return ORJSONResponse(FileResponseStructure(files=items).model_dump())


@file_router.get("/{id}/account/{ownerid}")
def get_file_route(
    ownerid: str,
    id: str,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    item = file_service.get_file(db, ownerid, id)
    return ORJSONResponse(FileResponseStructure(files=[item]).model_dump())


@file_router.get("/account/{ownerid}/download")
def download_route(
    body: list[str],
    ownerid: str,
    db: Session = Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    content, file = file_service.download(db, ownerid, body)

    if len(body) == 1 and file.type == FileType.FILE:
        return StreamingResponse(
            content,
            media_type=file.content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{file.filename}.{file.extension}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    return StreamingResponse(
        content,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="downloaded_content.zip"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


# @file_router.get("/{id}/account/{ownerid}/preview")
# def image_preview(ownerid: str, id: str, db: Session = Depends(client.get_session)):
#     url = item_read_serv.preview_serv(db, ownerid, id)

#     return ORJSONResponse(
#         FileResponseStructure(files=url).model_dump(),
#         headers={
#             "Cache-Control": "max-age=3600, private",
#         },
#     )


@file_router.put("/{id}/account/{ownerid}/name")
def update_filename_route(
    id: str,
    ownerid: str,
    name: str = Body(media_type="text/plain"),
    db=Depends(client.get_session),
    file_service: FileUpdateService = Depends(FileUpdateService),
):
    file = file_service.update_filename(db, id, ownerid, name)

    return ORJSONResponse(FileResponseStructure(files=[file]).model_dump())


@file_router.delete("/account/{ownerid}")
def delete_items_route(
    ownerid: str,
    body: list[str],
    db=Depends(client.get_session),
    file_service: FileDeleteService = Depends(FileDeleteService),
):
    file_service.delete_items(db, ownerid, body)
    return Response(status_code=200)


@file_router.get("/{id}/account/{ownerid}/breadcrumb")
def breadcrumb_route(
    id: str,
    ownerid: str,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    breadcrumb = file_service.get_breadcrumb(db, ownerid, id)
    return ORJSONResponse(breadcrumb)
