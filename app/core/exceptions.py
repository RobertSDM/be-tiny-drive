from typing import Literal


class DomainError(Exception):
    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status
        super().__init__(self.message)


class NotSupported(DomainError):
    def __init__(self):
        self.message = "The resource you are trying to access is not supported yet"
        super().__init__(self.message, 501)


class ProcessingPreview(DomainError):
    def __init__(self):
        self.message = "The requested preview still processing. Wait a few seconds"
        super().__init__(self.message, 202)


class AccountAlreadyExists(DomainError):
    def __init__(self):
        self.message = f"The user already exists"
        super().__init__(self.message, 409)


class ParentNotFound(DomainError):
    def __init__(self):
        self.message = f"The parent was not found"
        super().__init__(self.message, 404)


class NotFound(DomainError):
    def __init__(self, message):
        super().__init__(message, 404)


class FileNotFound(NotFound):
    def __init__(self):
        super().__init__(f"The file not found")


class FileDeleteError(DomainError):
    def __init__(self):
        self.message = f"Error deleting the item"
        super().__init__(self.message, 500)


class FileBeParent(DomainError):
    def __init__(self):
        self.message = f"A file cannot be parent"
        super().__init__(self.message, 409)


class FileAlreadyExists(DomainError):
    def __init__(self, name: str, type_: Literal["file", "folder"]):
        self.message = f"The {type_} named '{name}' already exists in the folder"
        super().__init__(self.message, 409)


class AccountNotExists(DomainError):
    def __init__(self):
        self.message = f"The account don't exist"
        super().__init__(self.message, 404)


class AccountRegistrationError(DomainError):
    def __init__(self):
        self.message = "Error registring the user"
        super().__init__(self.message, 500)


class InvalidPassword(DomainError):
    def __init__(self):
        self.message = f"The password is invalid"
        super().__init__(self.message, 422)


class NoAuthorizationHeader(DomainError):
    def __init__(self):
        self.message = "The authorization header was not present in the request"
        super().__init__(self.message, 401)


class InvalidFileToPreview(DomainError):
    def __init__(self):
        self.message = "The item is not elegible for a preview"
        super().__init__(self.message, 501)


class IndentityMismatch(DomainError):
    def __init__(self):
        self.message = "Account mismatch"
        super().__init__(self.message, 409)


class InvalidJWTToken(DomainError):
    def __init__(self):
        self.message = "The token is invalid"
        super().__init__(self.message, 401)


class JWTTokenExpired(DomainError):
    def __init__(self):
        self.message = "The token has expired"
        super().__init__(self.message, 401)
