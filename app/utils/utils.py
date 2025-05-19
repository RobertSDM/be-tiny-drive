import math


def normalize_file_size(byte_size: int):
    prefix = ["b", "Kb", "Mb", "Gb"]

    pos_prefix = 0
    devided_byte = byte_size

    while devided_byte >= 1024 and pos_prefix < len(prefix) - 1:
        devided_byte /= 1024
        pos_prefix += 1

    return math.ceil(devided_byte), prefix[pos_prefix]


def make_bucket_path(ownerid: str, path: str, name: str):
    """
    Make the bucket path for a storage item file
    """

    folders = "/".join(path.split("/")[:-1])
    item_path = f"{folders}" if len(folders) > 0 else ""

    return f"user-{ownerid}/drive{"/" if len(folders) > 0 else ""}{item_path}/{name}"
