from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.schemas import DefaultResponse, Error
from app.core.validation_errors import ItemValidationError

CUSTOM_VALIDATION_MSG = {
    "string_too_short": "The {field} is too short",
    "string_too_long": "The {field} is too long",
    "string_pattern_mismatch": "The {field} is not a valid {field}",
}


def pydantic_error_handler(request: Request, exc: RequestValidationError):
    error_msgs = [
        CUSTOM_VALIDATION_MSG[error["type"]].format(field=error["loc"][1])
        for error in exc.errors()
    ]

    return JSONResponse(
        DefaultResponse(error=Error(message=error_msgs), success=False).model_dump(),
        status_code=422,
    )


def validation_error_handler(request: Request, exc: ItemValidationError):
    print(exc.message)

    return JSONResponse(
        DefaultResponse(
            error=Error(message=exc.message),
        ).model_dump(),
        status_code=exc.status,
    )
