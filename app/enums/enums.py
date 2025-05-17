from enum import Enum


class Mode(Enum):
    PROD = "prod"
    DEV = "dev"


class ItemType(Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"
