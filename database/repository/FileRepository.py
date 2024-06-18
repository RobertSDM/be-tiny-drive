from sqlalchemy.orm import joinedload, Session
from sqlalchemy import select
from service.decorator.time_spend import time_spent
from service.logging_config import logger
from database.models.FolderModel import Folder
from ..models.FileModel import File, FileData
import time

@time_spent
def find_all_files (db):
    return db.query(File).options(joinedload(File.fileData)).all()

def find_by_file_id(id):
    pass

def find_by_file_id_download(db, id):

    fileData_subq = (select(
            FileData.byteData,
            FileData.file_id
        ).select_from(FileData)
        .subquery())
        
    file_join_fileData = (select(
        File.id,
        File.fullname,
        fileData_subq.c.byteData
    )
    .join(fileData_subq, File.id == fileData_subq.c.file_id)
    .where(File.id == id))

    file = db.execute(file_join_fileData).mappings().fetchone()

    return file
    

def save_file (
    db,
    name,
    extension,
    byteData,
    byteSize,
    prefix,
    folderId: str,
):
    file = File(name, extension, byteSize, prefix, byteData, folderId)
    
    db.add(file)
    db.commit()

    return file

def files_with_no_parent(db: Session) -> list:

    files = db.query(File).where(File.folder == None).all()

    folders = db.query(Folder).all()

    return [files, folders]

def files_by_folder(db: Session, folderId: str) -> list:
    files = db.query(File).where(File.folder_id == folderId).all()

    return files
