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


class ItemType(Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"
