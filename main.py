from fastapi import FastAPI
from api.exeption_handling import domain_error_handler
from api.routes.item_route import item_router
from api.routes.auth_route import auth_router
from fastapi.middleware.cors import CORSMiddleware
from core.exeptions import DomainError, ItemExistsInFolder
from utils.logging_config import logger
from constants.env_definitions import debug, host, origins, port
import uvicorn

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


app.include_router(item_router, prefix="/item")
app.include_router(auth_router, prefix="/auth")

app.add_exception_handler(DomainError, domain_error_handler)

if __name__ == "__main__":
    logger.info("App stated on -> " + ":" + port)
    uvicorn.run("main:app", host=host, port=int(port), reload=True, log_level=debug, use_colors=True)
