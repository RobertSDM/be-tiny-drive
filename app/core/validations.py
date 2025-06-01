import re


name_regex = r"^[a-zA-Z0-9._\- ]+$"
max_folder_depth = 3
# max_files = 15 # rate limit maybe?


def validate_item_name(name: str) -> bool:
    if len(name) < 4 or len(name) > 50 or name == "":
        return False

    return re.match(name_regex, name)
