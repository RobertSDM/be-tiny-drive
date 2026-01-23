from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import FileValidationError
from app.core.schemas import ErrorResponse


def pydantic_error_handler(request: Request, exc: RequestValidationError):
    print(exc.errors())
    return JSONResponse(
        ErrorResponse(message="Error on server side, not your fault").model_dump(),
        status_code=500,
    )


def validation_error_handler(request: Request, exc: FileValidationError):
    return JSONResponse(
        ErrorResponse(message=exc.message).model_dump(),
        status_code=exc.status,
    )
