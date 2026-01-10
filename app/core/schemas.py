from datetime import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict

from app.core.enums import ProcessingState

T = TypeVar("T")

# ENUMS
from enum import Enum


class Sort(Enum):
    NAME = "name"
    UPDATE_DATE = "upddate"
    CREATION_DATE = "creadate"


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


class Mode(Enum):
    PROD = "prod"
    DEV = "dev"


class ProcessingState(Enum):
    """
    STABLE set when the file is done from the main processing and is returned to the client. The rest of the processing happens in background (create preview, thumbnail, etc...)

    COMPLETE set when all the file processing is completed
    """

    STABLE = "STABLE"
    COMPLETE = "COMPLETE"


class ItemType(Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


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
    processing_state: ProcessingState
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


class RegisterPassword(BaseModel):
    id: str
    creation_date: datetime
    email: str


class FailureAndSuccess(BaseModel, Generic[T]):
    failures: list[T]
    successes: list[T]


class LoginReturn(BaseModel):
    token: str
    user: AccountModel


# API


class Error(BaseModel):
    message: str | list | dict


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


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
