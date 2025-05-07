from ast import TypeVar
from email import message
from pydantic import BaseModel, ConfigDict
from typing import Generic, Optional

from database.models.enums.content_type import ItemType
from database.models.item_model import Item

# ORM Models


class ItemModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extension: str
    path: str
    size: int
    size_prefix: str
    type: str


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str


# Schemas


class LoginReturn(BaseModel):
    token: str
    user: UserModel


# API


class Error(BaseModel):
    message: str


T = TypeVar("T")


class DefaultResponse[T](BaseModel):
    data: list[T] | T | None = None
    error: Error | None = None
    success: bool = True


class AuthResponse(DefaultResponse[UserModel]):
    token: str | None = None


class ItemResponse(DefaultResponse[ItemModel]):
    count: int = 0


class UserResponse(DefaultResponse[UserModel]):
    pass


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
