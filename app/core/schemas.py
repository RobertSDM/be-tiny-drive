from datetime import datetime
from typing import List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

# ENUMS
from enum import Enum


class SortColumn(Enum):
    NAME = "name"
    UPDATED_AT = "upddate"
    CREATED_AT = "creadate"


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


class Mode(Enum):
    PROD = "prod"
    DEV = "dev"


class FileType(Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


# DTOs


class FileReturnable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    extension: str
    size: int
    size_prefix: str
    content_type: str
    type: FileType
    parent: Optional["FileReturnable"]
    content_type: str
    updated_at: datetime
    created_at: datetime


class AccountReturnable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: str
    created_at: datetime


class FileResponseStructure(BaseModel):
    files: List[FileReturnable]
    parent: Optional[FileReturnable] = None
    message: Optional[str] = ""


class ErrorResponse(BaseModel):
    message: str
    description: str = ""
