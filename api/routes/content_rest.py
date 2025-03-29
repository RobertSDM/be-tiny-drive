import json
from fastapi import APIRouter, Depends, Response
from utils.convert_types import (
    convert_content_to_json,
    convert_file_to_response_file,
    convert_folder_to_response_folder,
)
from database.db_engine import get_session
from database.repositories.content_repository import find_all_content
from service.content_search_serv import content_search_serv

content_router = APIRouter()


@content_router.get("/by/folder/{id}/{owner_id}", status_code=200)
def __find_all_content_by_folder(
    id: str, owner_id: str, p: int = 1, db=Depends(get_session)
):

    if p < 1:
        p = 1

    result = find_all_content(db, owner_id, id, p)

    conv_content = convert_content_to_json(
        result["content"], result["requested_folder"]
    )

    conv_content.update({"totalCount": result["total_count"], "page": p})

    if len(result) > 0:
        return Response(status_code=200, content=json.dumps(conv_content))
    else:
        return Response(status_code=204)


@content_router.get("/all/{owner_id}")
def __find_all_content(owner_id: str, p: int = 1, db=Depends(get_session)):
    if p < 1:
        p = 1

    result = find_all_content(db, owner_id, page=p)

    conv_content = convert_content_to_json(
        result["content"], result["requested_folder"]
    )

    conv_content.update({"totalCount": result["total_count"]})

    if len(result["content"]) > 0:
        return Response(status_code=200, content=json.dumps(conv_content))
    else:
        return Response(status_code=204)


@content_router.get("/search/{owner_id}", status_code=200)
def __search_content(
    q: str, owner_id: str, type: str | None = None, db=Depends(get_session)
):
    def convert_file_to_response_file_search(files):
        res = []

        for i in files:
            res.append(convert_file_to_response_file(i, True))
        return res

    def convert_folder_to_response_folder_search(folders):
        res = []

        for i in folders:
            res.append(convert_folder_to_response_folder(i, True))
        return res

    content = content_search_serv(db, q, owner_id, type)

    conv_content = {
        "files": convert_file_to_response_file_search(content["files"]),
        "folders": convert_folder_to_response_folder_search(content["folders"]),
    }

    if len(content) > 0:
        return Response(
            status_code=200, content=json.dumps({"msg": None, "data": conv_content})
        )
    else:
        return Response(
            status_code=204, content=json.dumps({"msg": None, "data": None})
        )
