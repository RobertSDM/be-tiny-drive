import json
from fastapi import APIRouter, Depends, Response
from controller.convert.convert_types import convert_content_to_json
from database.init_database import get_session
from database.repository.file_repository import find_by_folder, find_with_no_parent

content_router = APIRouter()


@content_router.get("/by/folder/{id}/{owner_id}", status_code=200)
def __find_content_by_folder(id: str, owner_id: str, db=Depends(get_session)):
    content = find_by_folder(db, id, owner_id)

    conv_content = convert_content_to_json(content)

    if len(content) > 0:
        return Response(
            status_code=200, content=json.dumps({"msg": None, "data": conv_content})
        )
    else:
        return Response(status_code=204)


@content_router.get("/all/{owner_id}")
def __find_file_with_no_parent(owner_id: str, db=Depends(get_session)):
    content = find_with_no_parent(db, owner_id)

    conv_content = convert_content_to_json(content)

    if len(content) > 0:
        return Response(
            status_code=200, content=json.dumps({"msg": None, "data": conv_content})
        )
    else:
        return Response(
            status_code=204, content=json.dumps({"msg": None, "data": None})
        )
