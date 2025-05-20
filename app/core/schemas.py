import datetime
from typing import TypeVar
from pydantic import BaseModel, ConfigDict


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


class AccountModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: str
    creation_date: datetime.datetime


# Schemas


class LoginReturn(BaseModel):
    token: str
    user: AccountModel


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


class AccountResponse(SingleResponse[AccountModel]):
    pass


class AuthRegisterResponse(SingleResponse[AccountModel]):
    pass


class AuthLoginResponse(SingleResponse[AccountModel]):
    access_token: str
    refresh_token: str


class ListItemResponse(ListResponse[ItemModel]):
    pass


class SingleItemResponse(SingleResponse[ItemModel]):
    pass


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
