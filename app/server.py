import uvicorn

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.schemas import Mode
from app.middlewares.exception_middlewares import (
    domain_error_handler,
    pydantic_error_handler,
)
from app.features.auth.auth_router import auth_router
from app.features.file.file_router import file_router
from app.features.account.account_router import account_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import DomainError
from app.core.constants import (
    HOST,
    LOG_LEVEL,
    MODE,
    ORIGINS,
    PORT,
)
from app.middlewares.authorization_middleware import authorization_middleware

app = FastAPI(
    title="Tiny Drive",
    description="Backend API for tiny-drive project",
    dependencies=[Depends(authorization_middleware)],
)

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
app.include_router(file_router, prefix="/files")
app.include_router(account_router, prefix="/account")

app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(RequestValidationError, pydantic_error_handler)


@app.get("/")
def root():
    return "I'm alive!"

@app.get("/send/{message}")
def s(message: str):
    from app.lib.rabbitmq import send
    send("file_processing", message)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        reload=MODE == Mode.DEV.value,
    )
