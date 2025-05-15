from typing import TypeVar
from pydantic import BaseModel, ConfigDict

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
    update_date: float
    creation_date: float


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
