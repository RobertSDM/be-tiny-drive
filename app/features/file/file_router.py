from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Query, UploadFile
from fastapi.responses import (
    ORJSONResponse,
    StreamingResponse,
    Response,
)
from pydantic import BaseModel
from pytest import Session

from app.core.schemas import FileResponseStructure
from app.database.models import FileModel
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
    filename: str


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
    file = file_service.save_folder(db, ownerid, parentid, body.filename)

    return ORJSONResponse(FileResponseStructure(files=[file]).model_dump())


@file_router.post("/account/{ownerid}/parent")
@file_router.post("/account/{ownerid}/parent/{parentid}")
def save_file_route(
    filedata: List[UploadFile],
    ownerid: str,
    background_tasks: BackgroundTasks,
    parentid: Optional[str] = None,
    db=Depends(client.get_session),
    file_service: FileWriteService = Depends(FileWriteService),
):
    files: List[FileModel] = file_service.save_file(db, filedata, ownerid, parentid)

    files_to_process = [file for file in files if not file.is_dir]

    background_tasks.add_task(
        lambda: file_service.create_preview(ownerid, files_to_process)
    )

    return ORJSONResponse(
        FileResponseStructure(
            files=[file for file in files if file.parentid == parentid]
        ).model_dump()
    )


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
    files = file_service.search(
        db, ownerid, q, type_ == FileType.FOLDER if type_ is not None else None
    )

    return ORJSONResponse(FileResponseStructure(files=files).model_dump())


@file_router.get("/{id}/account/{ownerid}")
def get_file_route(
    ownerid: str,
    id: str,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    item = file_service.get_file(db, ownerid, id)
    return ORJSONResponse(FileResponseStructure(files=[item]).model_dump())


class DownloadRequest(BaseModel):
    fileids: List[str]


@file_router.post("/account/{ownerid}/download")
def download_route(
    body: DownloadRequest,
    ownerid: str,
    db: Session = Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    content, file = file_service.download(db, ownerid, body.fileids)

    if len(body.fileids) == 1 and not file.is_dir:
        return StreamingResponse(
            content,
            media_type=file.content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{file.filename}{file.extension}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    return StreamingResponse(
        content,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{f'{file.filename}.zip' if file.is_dir else 'content.zip'}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


class PreviewResponse(BaseModel):
    url: str


@file_router.get("/{id_}/account/{ownerid}/preview")
def image_preview(
    ownerid: str,
    id_: str,
    db: Session = Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    url = file_service.preview(db, ownerid, id_)

    return ORJSONResponse(
        PreviewResponse(url=url).model_dump(),
        headers={
            "Cache-Control": "max-age=3600, private",
        },
    )


class UpdateFilenameRequest(BaseModel):
    filename: str


@file_router.put("/{id}/account/{ownerid}/name")
def update_filename_route(
    id: str,
    ownerid: str,
    body: UpdateFilenameRequest,
    db=Depends(client.get_session),
    file_service: FileUpdateService = Depends(FileUpdateService),
):
    file = file_service.update_filename(db, id, ownerid, body.filename)

    return ORJSONResponse(FileResponseStructure(files=[file]).model_dump())


class DeleteItemsRequest(BaseModel):
    fileids: List[str]


@file_router.delete("/account/{ownerid}")
def delete_items_route(
    ownerid: str,
    body: DeleteItemsRequest,
    db=Depends(client.get_session),
    file_service: FileDeleteService = Depends(FileDeleteService),
):
    files = file_service.delete_files(db, ownerid, body.fileids)
    return ORJSONResponse(FileResponseStructure(files=files).model_dump())


@file_router.get("/{id}/account/{ownerid}/breadcrumb")
def breadcrumb_route(
    id: str,
    ownerid: str,
    db=Depends(client.get_session),
    file_service: FileReadService = Depends(FileReadService),
):
    breadcrumb = file_service.get_breadcrumb(db, ownerid, id)
    return ORJSONResponse([b.model_dump() for b in breadcrumb])
