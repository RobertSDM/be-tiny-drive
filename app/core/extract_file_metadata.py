from uuid import uuid4
from fastapi import UploadFile

from app.database.models.item_model import Item
from app.enums.enums import ItemType
from app.utils.utils import normalize_file_size


def generate_folders_paths(folders: list[str]) -> list[str]:
    paths = list()

    for f in folders:
        if len(paths) > 0:
            paths.append(f"{paths[-1]}/{f}")
        else:
            paths.append(f)

    return list(paths)


def create_items_from_path(
    file: UploadFile, ownerid: str, bucketid: str, parent_path: str
) -> tuple[list[Item], Item]:
    struct = list()

    fullpath: str = file.filename

    dirs: list[str] = fullpath.split("/")
    folders_paths: list[str] = generate_folders_paths(dirs[:-1])

    for path in folders_paths:
        folder = Item(
            extension="",
            parentid=None,
            size=0,
            size_prefix="",
            content_type="",
            bucketid=None,
            name=path.split("/")[-1],
            ownerid=ownerid,
            path=f"{parent_path}/{path}" if parent_path != "" else path,
            type=ItemType.FOLDER,
        )
        struct.append(folder)

    name = ".".join(dirs[-1].split(".")[:-1])
    extension = file.content_type.split("/")[1]
    normalized_size, prefix = normalize_file_size(file.size)

    item = Item(
        name=name,
        extension=extension,
        parentid=None,
        path=f"{parent_path}/{fullpath}" if parent_path != "" else fullpath,
        content_type=file.content_type,
        size=normalized_size,
        size_prefix=prefix,
        bucketid=bucketid,
        ownerid=ownerid,
        type=ItemType.FILE,
    )

    return struct, item
