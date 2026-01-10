import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.exception_handlers.domain_error import domain_error_handler

from app.api.exception_handlers.validation_error import (
    pydantic_error_handler,
    validation_error_handler,
)
from app.core.validation_errors import FileValidationError
from app.features.auth.auth_router import auth_router
from app.features.file.item_router import item_router
from app.features.account.auth_router import account_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import DomainError
from app.core.constants import LOG_LEVEL, HOST, ORIGINS, PORT

app = FastAPI(title="Tiny Drive", description="Backend API for tiny-drive project")

## Middlewares
# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)


app.include_router(auth_router, prefix="/auth")
app.include_router(item_router, prefix="/files")
app.include_router(account_router, prefix="/account")

app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(RequestValidationError, pydantic_error_handler)
app.add_exception_handler(FileValidationError, validation_error_handler)


@app.get("/")
def root():
    return "I'm alive!"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level=LOG_LEVEL,
        use_colors=True,
    )
