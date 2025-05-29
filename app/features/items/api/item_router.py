from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, Form, UploadFile
from fastapi.responses import FileResponse, ORJSONResponse, StreamingResponse
from pydantic import BaseModel
from pytest import Session

from app.core.schemas import (
    FailureAndSuccess,
    ListItemResponse,
    SingleItemResponse,
    SingleResponse,
)
from app.database.client.sqlalchemy_client import db_client
from app.enums.enums import ItemType, Sort, SortOrder
from app.features.items.services import (
    item_create_serv,
    item_delete_serv,
    item_read_serv,
    item_update_serv,
)
from app.middlewares.auth_middleware import auth_middleware


item_router = APIRouter(dependencies=[Depends(auth_middleware)])


@item_router.post("/save")
def save_file_route(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    ownerid: Annotated[str, Form()],
    parentid: Annotated[str | None, Form()] = None,
    db=Depends(db_client.get_session),
):
    item = item_create_serv.item_save_item_serv(db, file, ownerid, parentid)
    background_tasks.add_task(
        item_create_serv.item_create_preview_serv, db, item.ownerid, item.id
    )

    return ORJSONResponse(SingleItemResponse(data=item).model_dump())


class SaveFolderBody(BaseModel):
    name: str
    parentid: str | None
    ownerid: str


@item_router.post("/save/folder")
def save_folder_route(body: SaveFolderBody, db=Depends(db_client.get_session)):
    folder = item_create_serv.item_save_folder_serv(
        db, body.ownerid, body.name, body.parentid
    )

    return ORJSONResponse(SingleItemResponse(data=folder).model_dump())


@item_router.get("/all/{ownerid}")
def get_all_items_route(
    ownerid: str,
    p: int = 0,
    order: SortOrder = SortOrder.ASC,
    sort: Sort = Sort.NAME,
    db=Depends(db_client.get_session),
):
    items = item_read_serv.all_root_items_serv(db, ownerid, p, order, sort)

    return ORJSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/all/{ownerid}/{parentid}")
def get_all_item_in_folder_route(
    ownerid: str,
    parentid: str,
    p: int = 0,
    order: SortOrder = SortOrder.ASC,
    sort: Sort = Sort.NAME,
    db=Depends(db_client.get_session),
):
    items = item_read_serv.all_items_in_folder_serv(
        db, ownerid, parentid, p, order, sort
    )

    return ORJSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/search/{ownerid}")
def item_search_route(
    ownerid: str,
    q: str,
    type: ItemType | None = None,
    db: Session = Depends(db_client.get_session),
):
    items = item_read_serv.search_serv(db, ownerid, q, type)

    return ORJSONResponse(ListItemResponse(data=items, count=len(items)).model_dump())


@item_router.get("/{ownerid}/{id}")
def get_item_by_id_route(ownerid: str, id: str, db=Depends(db_client.get_session)):
    item = item_read_serv.item_by_id_serv(db, ownerid, id)

    return ORJSONResponse(SingleItemResponse(data=item).model_dump())


class DownloadManyFilesBody(BaseModel):
    fileids: list[str]


@item_router.get("/download/many/{ownerid}")
def download_many_files_route(
    body: DownloadManyFilesBody,
    ownerid: str,
    db: Session = Depends(db_client.get_session),
):
    zip = item_read_serv.download_many_serv(db, body.fileids, ownerid)

    return StreamingResponse(zip, media_type="application/zip")


@item_router.get("/download/folder/{ownerid}/{parentid}")
def donwload_folder_route(
    ownerid: str, parentid: str, db: Session = Depends(db_client.get_session)
):
    zip = item_read_serv.download_folder_serv(db, ownerid, parentid)

    return StreamingResponse(
        zip,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment;filename=downloaded_content",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@item_router.get("/download/{ownerid}/{id}")
def download_file_route(id: str, ownerid: str, db=Depends(db_client.get_session)):
    data, content_type, filename = item_read_serv.download_serv(db, id, ownerid)

    return StreamingResponse(
        data,
        media_type=content_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@item_router.get("/preview/{ownerid}/{id}")
def image_preview(ownerid: str, id: str, db: Session = Depends(db_client.get_session)):
    url = item_read_serv.preview_serv(db, ownerid, id)

    return ORJSONResponse(
        SingleResponse(data=url).model_dump(),
        headers={
            "Cache-Control": "max-age=3600, private",
        },
    )


class UpdateNameBody(BaseModel):
    name: str


@item_router.put("/update/{ownerid}/{id}/name")
def put_name_route(
    id: str, ownerid: str, body: UpdateNameBody, db=Depends(db_client.get_session)
):
    item = item_update_serv.item_update_name(db, id, ownerid, body.name)

    return ORJSONResponse(SingleItemResponse(data=item).model_dump())


class DeleteItemBody(BaseModel):
    itemids: list[str]


@item_router.delete("/delete/{ownerid}")
def delete_item_route(
    ownerid: str, body: DeleteItemBody, db=Depends(db_client.get_session)
):
    sucesses, failures = item_delete_serv.delete_items_serv(db, ownerid, body.itemids)

    return ORJSONResponse(
        SingleResponse(
            data=FailureAndSuccess(successes=sucesses, failures=failures)
        ).model_dump()
    )


@item_router.get("/breadcrumb/{ownerid}/{id}")
def breadcrumb_route(id: str, ownerid: str, db=Depends(db_client.get_session)):
    breadcrumb = item_read_serv.breadcrumb_serv(db, ownerid, id)

    return ORJSONResponse(
        ListItemResponse(data=breadcrumb, count=len(breadcrumb)).model_dump()
    )
