from fastapi import FastAPI
import uvicorn
from app.api.exeption_handling import domain_error_handler
from app.api.middlewares.auth_middleware import AuthMiddleware
from app.api.routes.item_route import item_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.exeptions import DomainError
from app.utils.logging_config import logger
from app.constants.env_definitions import debug, host, origins, port

app = FastAPI(title="Tiny Drive", description="Backend API for tiny-drive project")

## Middlewares
# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(item_router, "/item")
app.add_middleware(AuthMiddleware)
app.add_exception_handler(DomainError, domain_error_handler)

if __name__ == "__main__":
    logger.info("App stated on -> " + ":" + port)
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level=debug,
        use_colors=True,
    )
