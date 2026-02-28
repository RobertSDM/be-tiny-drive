from fastapi import APIRouter, Depends, Request
from fastapi.responses import ORJSONResponse
from server.app.middlewares.authorization_middleware import authorization_middleware

account_router = APIRouter(dependencies=[Depends(authorization_middleware)])


@account_router.get("/", response_class=ORJSONResponse)
def account(
    request: Request,
):
    return request.state.owner
