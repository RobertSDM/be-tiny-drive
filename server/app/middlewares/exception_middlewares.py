from fastapi import Request
from fastapi.exceptions import RequestValidationError

from server.app.core.schemas import ErrorResponse
from fastapi.responses import ORJSONResponse
from server.app.core.exceptions import DomainError


def pydantic_error_handler(_: Request, exc: RequestValidationError):
    print(exc)
    return ORJSONResponse(
        ErrorResponse(message="Error on server side, not your fault").model_dump(),
        status_code=500,
    )


def domain_error_handler(_: Request, exc: DomainError):
    return ORJSONResponse(
        status_code=exc.status,
        content=ErrorResponse(message=exc.message).model_dump(),
    )
