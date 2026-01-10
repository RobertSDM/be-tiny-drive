from enum import auto, IntFlag

from app.core.constants import MAX_RECURSIVE_DEPTH


class FileValidationCode(IntFlag):
    INVALID_NAME = auto()
    TO_DEEP = auto()


class FileValidationError(Exception):
    def __init__(self, message: str, code: FileValidationCode, status: int):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)


class InvalidFileName(FileValidationError):
    def __init__(self, name: str):
        self.message = f"The item name '{name}' is not valid. There are allowed only '_', '.', '-', letters, numbers and spaces"

        super().__init__(self.message, FileValidationCode.INVALID_NAME, 422)


class ItemToDeep(FileValidationError):
    def __init__(self, name: str):
        self.message = (
            f"The item '{name}' exceeds the maximum depth {MAX_RECURSIVE_DEPTH}"
        )

        super().__init__(self.message, FileValidationCode.TO_DEEP, 422)
