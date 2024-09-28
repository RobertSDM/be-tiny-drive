from pydantic import BaseModel
from typing import  Optional


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


class UserBase(BaseModel):
    id: str
    user_name: str
    email: str
    password: str
    saved_content_size: int


class ResponseFolderBase(BaseModel):
    id: str
    name: str
    folderC_id: str | None



class ResponseFile(BaseModel):
    id: str
    name: str
    fullname: str
    folder_id: str | None
    byteSize: int
    extension: str
    prefix: str


class ResponseUser(BaseModel):
    id: str
    user_name: str
    email: str


# Schemas

class Tray(BaseModel):
    tray: str

class UpdatedTray(BaseModel):
    id: str
    updatedTray: Tray

class FolderUpdate(BaseModel):
    name: str
    folder_id: str | None
    new_name: str
    parent_id: str | None


class FileUpdate(BaseModel):
    name: str
    extension: str
    folder_id: str | None
    new_name: str


class DefaultDefReponseContent(BaseModel):
    msg: str
    data: Optional[str]


class DefaultDefReponse(BaseModel):
    status: int
    content: DefaultDefReponseContent


class UserParamLoginSchema(BaseModel):
    email: str
    password: str


class UserParamRegisterSchema(BaseModel):
    email: str
    user_name: str
    password: str


class FileDataSchema(FileDataBase):
    file: FileBase
    owner: UserBase


class FolderSchema(FolderBase):
    folders: list[FolderBase]
    folder: FolderBase
    files: list[FileBase]
    owner: UserBase


class UserSchema(UserBase):
    files: list[FileBase]
    folders: list[FolderBase]


class FileSchema(FileBase):
    folder: FolderBase | None


class FolderBody(BaseModel):
    name: str
    parentId: str | None
    owner_id: str


class FileBody(BaseModel):
    name: str
    folderId: str | None
    extension: str
    byteData: str
    byteSize: int
    owner_id: str
