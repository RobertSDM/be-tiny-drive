from fastapi import FastAPI
import uvicorn
from app.api.exeption_handling.domain_error_handler import domain_error_handler

from app.features.auth.api.auth_router import auth_router
from app.features.items.api.item_router import item_router
from app.features.account.api.auth_router import account_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import DomainError
from app.constants.env import debug, host, origins, port

app = FastAPI(title="Tiny Drive", description="Backend API for tiny-drive project")

## Middlewares
# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)


app.include_router(auth_router, prefix="/auth")
app.include_router(item_router, prefix="/item")
app.include_router(account_router, prefix="/account")
app.add_exception_handler(DomainError, domain_error_handler)


@app.get("/")
def root():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level=debug,
        use_colors=True,
    )
