from typing import BinaryIO, TypeVar
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict

from app.enums.enums import ItemType

# ORM Models


class ItemModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    extension: str
    path: str
    size: int
    size_prefix: str
    type: str
    parentid: str | None
    update_date: float
    creation_date: float


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: str


# Schemas


class Metadata(BaseModel):
    name: str
    extension: str
    size: int
    size_prefix: str
    type: ItemType
    parentid: str | None
    ownerid: str
    bucketid: str
    path: str


class LoginReturn(BaseModel):
    token: str
    user: UserModel


# API


class Error(BaseModel):
    message: str


T = TypeVar("T")


class DefaultResponse(BaseModel):
    error: Error | None = None
    success: bool = True


class ListResponse[T](DefaultResponse):
    data: list[T]
    count: int


class SingleResponse[T](DefaultResponse):
    data: T


class AuthResponse(SingleResponse[UserModel]):
    token: str | None = None


class ListItemResponse(ListResponse[ItemModel]):
    pass


class SingleItemResponse(SingleResponse[ItemModel]):
    pass


class UserResponse(SingleResponse[UserModel]):
    pass


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
