from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exeptions import DomainError
from app.core.schemas import DefaultResponse, Error


def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status,
        content=DefaultResponse(
            success=False, error=Error(message=exc.message)
        ).model_dump(),
    )
