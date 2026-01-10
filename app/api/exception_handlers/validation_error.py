from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.schemas import ErrorResponse, FileResponseStructure
from app.core.validation_errors import FileValidationError


def pydantic_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        ErrorResponse(message="Error on server side, not your fault").model_dump(),
        status_code=500,
    )


def validation_error_handler(request: Request, exc: FileValidationError):
    print(exc.message)

    return JSONResponse(
        ErrorResponse(message=exc.message).model_dump(),
        status_code=exc.status,
    )
