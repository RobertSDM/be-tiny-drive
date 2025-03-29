import json
import math
from sqlalchemy.orm import Session, load_only, joinedload, lazyload
from sqlalchemy import and_, literal, func, select

from database.models.file_model import File
from database.models.folder_model import Folder
from project.variables.global_variables import TAKE_CONTENT_PER_PAGE


def find_all_content(
    db: Session,
    owner_id: str,
    folder_id: str = None,
    page: int = 1,
) -> list:
    requestedFolder = (
        db.query(Folder)
        .options(
            load_only(Folder.id, Folder.name, Folder.tray, Folder.folderC_id),
            joinedload(Folder.folder),
        )
        .filter(and_(Folder.id == folder_id, Folder.owner_id == owner_id))
        .first()
    )

    # Query para arquivos órfãos
    files = db.query(
        File.id.label("id"),
        File.name.label("name"),
        File.byteSize.label("byteSize"),
        File.type.label("type"),
        File.extension.label("extension"),
        literal(None).label("tray"),
        File.folder_id.label("folderC_id"),
        File.filename.label("fullname"),
        File.prefix.label("prefix"),
    ).filter(and_(File.folder_id == folder_id, File.owner_id == owner_id))

    # Query para pastas órfãs
    folders = db.query(
        Folder.id.label("id"),
        Folder.name.label("name"),
        literal(None).label("byteSize"),
        Folder._type.label("type"),
        literal(None).label("extension"),
        Folder.tray.label("tray"),
        Folder.folderC_id.label("folderC_id"),
        literal(None).label("fullname"),
        literal(None).label("prefix"),
    ).filter(and_(Folder.folderC_id == folder_id, Folder.owner_id == owner_id))

    total_count = math.ceil((files.count() + folders.count()) / TAKE_CONTENT_PER_PAGE)

    # Realiza a união das queries
    main_query = (
        select(files.union_all(folders).subquery())
        .limit(TAKE_CONTENT_PER_PAGE)
        .offset((page - 1) * TAKE_CONTENT_PER_PAGE)
        .order_by("name")
    )

    content = db.execute(main_query).all()

    return {
        "content": content,
        "requested_folder": requestedFolder if requestedFolder else None,
        "total_count": total_count,
    }
