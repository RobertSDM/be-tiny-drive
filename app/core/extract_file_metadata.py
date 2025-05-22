from functools import reduce
from uuid import uuid4
from fastapi import UploadFile

from app.database.models.item_model import Item
from app.enums.enums import ItemType
from app.utils.utils import normalize_file_size


def create_items_from_path(
    file_data: UploadFile, ownerid: str
) -> tuple[list[Item], Item]:
    folders = list()

    dirs: list[str] = file_data.filename.split("/")
    folder_names: list[str] = dirs[:-1]

    for name in folder_names:
        folder = Item(
            id=str(uuid4()),
            extension="",
            parentid=None,
            size=0,
            size_prefix="",
            content_type="",
            name=name,
            ownerid=ownerid,
            type=ItemType.FOLDER,
        )
        folders.append(folder)

    name_splited = dirs[-1].split(".")
    name = ".".join(name_splited[:-1]) if len(name_splited) > 1 else name_splited[0]
    extension = (
        f".{name_splited[-1]}"
        if len(name_splited) > 1 and name_splited[-1] != ""
        else ""
    )
    normalized_size, prefix = normalize_file_size(file_data.size)

    file = Item(
        id=str(uuid4()),
        name=name,
        extension=extension,
        parentid=None,
        content_type=file_data.content_type,
        size=normalized_size,
        size_prefix=prefix,
        ownerid=ownerid,
        type=ItemType.FILE,
    )

    return folders, file
