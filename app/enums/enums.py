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
