from fastapi import APIRouter, Depends, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from app.core.authentication_client_singleton import get_auth_service
from app.core.schemas import AccountDTO
from app.interfaces.authentication_interface import AuthenticationInterface
from app.lib.sqlalchemy import client
from app.features.account.services.account_serv import AccountService
from app.middlewares.authorization_middleware import authorization_middleware

account_router = APIRouter(dependencies=[Depends(authorization_middleware)])


@account_router.get("/", response_class=ORJSONResponse)
def account(
    request: Request,
):
    return request.state.owner
