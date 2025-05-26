from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

# ORM Models


class ItemModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    extension: str
    size: int
    size_prefix: str
    content_type: str
    type: str
    parentid: str | None
    update_date: datetime
    creation_date: datetime


class AccountModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: str
    creation_date: datetime


# Schemas


class FailureAndSuccess(BaseModel, Generic[T]):
    failures: list[T]
    successes: list[T]


class LoginReturn(BaseModel):
    token: str
    user: AccountModel


# API


class Error(BaseModel):
    message: str


class DefaultResponse(BaseModel):
    error: Error | None = None
    success: bool = True


class FailureAndSuccess(BaseModel, Generic[T]):
    failures: list[T]
    successes: list[T]


class ListResponse(DefaultResponse, Generic[T]):
    data: list[T]
    count: int


class SingleResponse(DefaultResponse, Generic[T]):
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
