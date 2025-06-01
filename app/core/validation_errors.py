from enum import auto, IntFlag
from app.core.validations import max_folder_depth


class ItemValidationCode(IntFlag):
    INVALID_NAME = auto()
    TO_DEEP = auto()


class ItemValidationError(Exception):
    def __init__(self, message: str, code: ItemValidationCode, status: int):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)


class InvalidItemName(ItemValidationError):
    def __init__(self, name: str):
        self.message = f"The item name '{name}' is not valid. There are allowed only '_', '.', '-', letters, numbers and spaces"

        super().__init__(self.message, ItemValidationCode.INVALID_NAME, 422)


class ItemToDeep(ItemValidationError):
    def __init__(self, name: str):
        self.message = (
            f"The item '{name}' exceeds the maximum depth {max_folder_depth}"
        )

        super().__init__(self.message, ItemValidationCode.TO_DEEP, 422)
