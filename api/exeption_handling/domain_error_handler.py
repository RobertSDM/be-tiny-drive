from fastapi import Request
from fastapi.responses import JSONResponse
from core.exeptions import DomainError
from core.schemas import DefaultResponse, Error


def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status,
        content=DefaultResponse(
            success=False, error=Error(message=exc.message)
        ).model_dump(),
    )
