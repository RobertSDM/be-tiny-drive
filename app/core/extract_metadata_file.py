from fastapi import UploadFile

from app.core.schemas import Metadata
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


def create_file_structure(
    file: UploadFile, path: str, ownerid: str, bucketid: str
) -> tuple[list[Item], Item]:
    struct = list()

    wholepath: str = path
    if len(wholepath) == 0:
        wholepath = file.filename

    dirs: list[str] = wholepath.split("/")
    folders_paths: list[str] = generate_folders_paths(dirs[:-1])

    for f in folders_paths:
        folder = Item(
            extension="",
            parentid=None,
            size=0,
            size_prefix="",
            bucketid=None,
            name=f.split("/")[-1],
            ownerid=ownerid,
            path=f,
            type=ItemType.FOLDER,
        )
        struct.append(folder)

    extension = file.content_type.split("/")[1]
    normalized_size, prefix = normalize_file_size(file.size)

    item = Item(
        name=file.filename,
        extension=extension,
        parentid=None,
        path=wholepath,
        size=normalized_size,
        size_prefix=prefix,
        bucketid=bucketid,
        ownerid=ownerid,
        type=ItemType.FILE,
    )

    return struct, item
