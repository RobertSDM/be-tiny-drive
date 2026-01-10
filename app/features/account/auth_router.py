from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from app.core.schemas import AccountReturnable
from app.lib.sqlalchemy import client
from app.features.account.services.account_serv import account_get_serv
from app.middlewares.authorization_middleware import authorization_middleware

account_router = APIRouter(dependencies=[Depends(authorization_middleware)])


@account_router.get("/{id}")
def account_get(id: str, db: Session = Depends(client.get_session)):
    account = account_get_serv(db, id)
    return ORJSONResponse(AccountReturnable(data=account).model_dump())
