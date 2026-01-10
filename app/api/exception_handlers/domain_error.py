from fastapi import Request
from fastapi.responses import ORJSONResponse
from app.core.exceptions import DomainError
from app.core.schemas import ErrorResponse, FileResponseStructure


def domain_error_handler(request: Request, exc: DomainError):
    return ORJSONResponse(
        status_code=exc.status,
        content=ErrorResponse(message=exc.message).model_dump(),
    )
