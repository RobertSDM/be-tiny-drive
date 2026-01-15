from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, UploadFile
from fastapi.responses import ORJSONResponse, StreamingResponse, Response
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


@file_router.post("/")
def save_file_route(
    file: UploadFile,
    # background_tasks: BackgroundTasks,
    ownerid: Annotated[str, Form()],
    parentid: Annotated[str | None, Form()] = None,
    db=Depends(client.get_session),
    file_service: FileWriteService = Depends(FileWriteService),
):
    file = file_service.save_file(db, file, ownerid, parentid)
    # if item.type == FileType.FILE:
    #     background_tasks.add_task(
    #         file_service.item_create_preview_serv, db, ownerid, item.id
    #     )

    return ORJSONResponse(FileResponseStructure(files=[file]).model_dump())


@file_router.get("/{ownerid}")
def get_items_route(
    ownerid: str,
    p: int = 0,
    order: SortOrder = SortOrder.ASC,
    sort: SortColumn = SortColumn.NAME,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    items = file_service.get_files(db, ownerid, p, order, sort)
    return ORJSONResponse(FileResponseStructure(files=items).model_dump())


@file_router.get("/folder/{parentid}/account/{ownerid}")
def get_files_in_folder_route(
    ownerid: str,
    parentid: str,
    p: int = 0,
    order: SortOrder = SortOrder.ASC,
    sort: SortColumn = SortColumn.NAME,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    items = file_service.get_files_in_folder(db, ownerid, parentid, p, order, sort)
    return ORJSONResponse(FileResponseStructure(files=items).model_dump())


# @file_router.get("/{ownerid}/search")
# def item_search_route(
#     ownerid: str,
#     q: str,
#     type: FileType | None = None,
#     db: Session = Depends(client.get_session),
# ):
#     items = search_service(db, ownerid, q, type)

#     return ORJSONResponse(FileResponseStructure(files=items).model_dump())


@file_router.get("/{id}/account/{ownerid}")
def get_file_route(
    ownerid: str,
    id: str,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    item = file_service.get_file(db, ownerid, id)
    return ORJSONResponse(FileResponseStructure(files=[item]).model_dump())


@file_router.get("/{ownerid}/download")
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


@file_router.delete("/{ownerid}")
def delete_items_route(
    ownerid: str,
    body: list[str],
    db=Depends(client.get_session),
    file_service: FileDeleteService = Depends(FileDeleteService),
):
    file_service.delete_items(db, ownerid, body)
    return Response(status_code=200)


@file_router.get("/{id}/account}/{ownerid}/breadcrumb")
def breadcrumb_route(
    id: str,
    ownerid: str,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    breadcrumb = file_service.get_breadcrumb(db, ownerid, id)
    return ORJSONResponse(FileResponseStructure(files=breadcrumb).model_dump())
