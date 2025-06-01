class DomainError(Exception):
    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status
        super().__init__(self.message)


class FeatureNotSupported(DomainError):
    def __init__(self):
        self.message = "Feature not supported yet"
        super().__init__(self.message, 500)


class PreviewStillProcessing(DomainError):
    def __init__(self):
        self.message = "The requested preview still processing. Wait a few seconds"
        super().__init__(self.message, 202)


class ItemKeyExistsInStorage(DomainError):
    def __init__(self):
        self.message = "Error saving the file"
        super().__init__(self.message, 500)


class AccountAlreadyExists(DomainError):
    def __init__(self):
        self.message = f"The user already exists"
        super().__init__(self.message, 409)


class ParentFolderNotFound(DomainError):
    def __init__(self):
        self.message = f"The parent folder was not found"
        super().__init__(self.message, 404)


class ItemNotFound(DomainError):
    def __init__(self):
        self.message = f"The item was not found"
        super().__init__(self.message, 404)


class ItemDeleteError(DomainError):
    def __init__(self):
        self.message = f"Error deleting the item"
        super().__init__(self.message, 500)


class FileCannotBeParent(DomainError):
    def __init__(self):
        self.message = f"A file cannot be parent of a file or folder"
        super().__init__(self.message, 409)


class ItemExistsInFolder(DomainError):
    def __init__(self, name: str, type: str):
        self.message = f"The {type.lower()} named '{name}' already exists in the folder"
        super().__init__(self.message, 409)


class AccountDoesNotExists(DomainError):
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
        super().__init__(self.message, 422)


class InvalidItemToPreview(DomainError):
    def __init__(self):
        self.message = "The item is not elegible to preview"
        super().__init__(self.message, 422)


class IndentityMismatch(DomainError):

    def __init__(self):
        self.message = "Account mismatch"
        super().__init__(self.message, 401)


class InvalidJWTToken(DomainError):
    def __init__(self):
        self.message = "The token is invalid"
        super().__init__(self.message, 422)


class JWTTokenExpired(DomainError):
    def __init__(self):
        self.message = "The token has expired"
        super().__init__(self.message, 401)
