class DomainError(Exception):
    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status
        super().__init__(self.message)


class AccountAlreadyExists(DomainError):
    def __init__(self):
        self.message = f"the user already exists"
        super().__init__(self.message, 409)


class ParentFolderNotFound(DomainError):
    def __init__(self):
        self.message = f"the parent folder was not found"
        super().__init__(self.message, 404)


class ItemNotFound(DomainError):
    def __init__(self):
        self.message = f"the item was not found"
        super().__init__(self.message, 404)


class ItemDeleteError(DomainError):
    def __init__(self):
        self.message = f"error deleting the item"
        super().__init__(self.message, 500)


class FileCannotBeParent(DomainError):
    def __init__(self):
        self.message = f"a file cannot be parent of a file or folder"
        super().__init__(self.message, 409)


class ItemExistsInFolder(DomainError):
    def __init__(self, name: str, type: str):
        self.message = f"the {type.lower()} named '{name}' already exists in the folder"
        super().__init__(self.message, 409)


class AccountDoesNotExists(DomainError):
    def __init__(self):
        self.message = f"the account don't exist"
        super().__init__(self.message, 404)


class AccountRegistrationError(DomainError):
    def __init__(self):
        self.message = "error registring the user"
        super().__init__(self.message, 500)


class InvalidPassword(DomainError):
    def __init__(self):
        self.message = f"the password is invalid"
        super().__init__(self.message, 422)


class NoAuthorizationHeader(DomainError):
    def __init__(self):
        self.message = "the authorization header was not present in the request"
        super().__init__(self.message, 422)


class InvalidItemToPreview(DomainError):
    def __init__(self):
        self.message = "the item is not elegible to preview"
        super().__init__(self.message, 422)


class IndentityMismatch(DomainError):

    def __init__(self):
        self.message = "account mismatch"
        super().__init__(self.message, 401)


class InvalidJWTToken(DomainError):
    def __init__(self):
        self.message = "the token is invalid"
        super().__init__(self.message, 422)


class JWTTokenExpired(DomainError):
    def __init__(self):
        self.message = "the token has expired"
        super().__init__(self.message, 401)
