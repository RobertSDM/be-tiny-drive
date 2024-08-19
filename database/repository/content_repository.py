from sqlalchemy.orm import Session, load_only, lazyload, Bundle
from sqlalchemy import and_, select, union

from database.models.file_model import File
from database.models.folder_model import Folder


def find_with_no_parent(db: Session, owner_id: str) -> list:
    files = (
        db.query(File)
        .options(
            load_only(
                File.id,
                File.extension,
                File.name,
                File.byteSize,
                File.fullname,
                File.prefix,
            ),
            lazyload(File.fileData),
        )
        .filter(and_(File.folder_id == None, File.owner_id == owner_id))
        .all()
    )

    folders = (
        db.query(Folder)
        .filter(and_(Folder.folderC_id == None, Folder.owner_id == owner_id))
        .all()
    )

    return {"files": files, "folders": folders}
