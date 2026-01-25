from typing import Literal


class DomainError(Exception):
    """
    Represents an error from business logic
    """

    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status
        super().__init__(self.message)


class NotSupported(DomainError):
    def __init__(self):
        self.message = "The resource you are trying to access is not supported yet"
        super().__init__(self.message, 501)


class AccountAlreadyExists(DomainError):
    def __init__(self):
        self.message = f"The user already exists"
        super().__init__(self.message, 409)


class FolderNotFound(DomainError):
    def __init__(self):
        super().__init__("The parent was not found", 404)


class FileNotFound(DomainError):
    def __init__(self):
        super().__init__(f"The file not found")


class FileDeleteError(DomainError):
    def __init__(self):
        super().__init__("Error while deleting", 500)


class FileNotBeParent(DomainError):
    def __init__(self):
        super().__init__("A file cannot be a parent", 409)


class FileAlreadyExists(DomainError):
    def __init__(self, name: str, type_: Literal["file", "folder"]):
        self.message = f"The {type_} named '{name}' already exists in the folder"
        super().__init__(self.message, 409)


class AccountNotExists(DomainError):
    def __init__(self):
        super().__init__("The account don't exist", 404)


class AccountRegistrationError(DomainError):
    def __init__(self):
        super().__init__("Error registering the account", 500)


class NoAuthorizationHeader(DomainError):
    def __init__(self):
        super().__init__("The authorization header was not present in the request", 401)


class PreviewNotSupported(DomainError):
    def __init__(self):
        super().__init__(
            "TinyDrive don't support previews for this file extension", 501
        )


class PreviewNotFound(DomainError):
    def __init__(self):
        super().__init__(
            "Preview not found.", 501
        )


class AccountMismatch(DomainError):
    def __init__(self):
        super().__init__("Account mismatch", 409)


class InvalidJWTToken(DomainError):
    def __init__(self):
        super().__init__("The token is invalid", 401)


class JWTTokenExpired(DomainError):
    def __init__(self):
        super().__init__("The token has expired", 401)


class InvalidFileName(DomainError):
    def __init__(self, name: str):
        super().__init__(
            f'The filename "{name}" is not valid. The characters: "\\", "/", ":", "*", "?", \'"\', "<", ">" and "|", are not allowed',
            422,
        )


class WrongAuthData(DomainError):
    def __init__(self):
        super().__init__("Email or password are wrong", 422)
