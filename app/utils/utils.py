import math
import re
from typing import Literal


def byte_formatting(byte_size: int):
    """
    Format the size to be more readable
    """

    prefix = ["B", "KB", "MB", "GB"]
    size = byte_size

    for p in prefix:
        if size < 1024:
            return math.ceil(size), p

        size /= 1024


def make_file_bucket_path(
    ownerid: str,
    fileid: str,
    type_: Literal["file", "preview", "trash+preview", "trash+file"],
) -> str:
    """
    Make the bucket path for the file storage
    """

    match type_:
        case "file":
            return f"user-{ownerid}/drive/{fileid}"
        case "preview":
            return f"user-{ownerid}/preview/{fileid}"
        case "trash+file":
            return f"user-{ownerid}/trash/drive/{fileid}"
        case "trash+preview":
            return f"user-{ownerid}/trash/preview/{fileid}"


def validate_filename(name: str) -> bool:

    name_regex = r"^[\^\<\>\*\?\\\|\"\'\:]$"
    # 260 is the maximum filename length in windows.
    # It's the largest of other OS
    if name == "" or len(name) > 260:
        return False

    return re.match(name_regex, name) is None
