from pydantic import BaseModel
from typing import Optional


class FileDataBase(BaseModel):
    id: str
    byteData: str
    file_id: str

    class Config:
        from_attributes = True

class FolderBase(BaseModel):
    id: str
    name: str
    _type: str
    folderC_id: str
    
    class Config:
        from_attributes = True

class FileBase(BaseModel):
    id: str
    name: str
    _type: str
    fullname: str
    folder_id: str | None
    byteSize: int
    extension: str
    prefix: str

    class Config:
        from_attributes = True


class ResponseFolderBase(BaseModel):
    id: str
    name: str
    folderC_id: str | None

class ResponseFolder(ResponseFolderBase):
    folder: ResponseFolderBase | None

class ResponseFile(BaseModel):
    id: str
    name: str
    fullname: str
    folder_id: str | None
    folder: ResponseFolder | None
    byteSize: int
    extension: str
    prefix: str
    
## Schemas

class FileDataSchema(FileDataBase):
    file: FileBase

class FolderSchema(FolderBase):
    folders: list[FolderBase]
    folder: FolderBase
    files: list[FileBase]



class FileSchema(FileBase):
    folder: FolderBase | None

class FolderBody(BaseModel):
    name: str
    parentId: str | None

class FileBody(BaseModel):
    name: str
    folderId: str | None
    extension: str
    byteData: str
    byteSize: int