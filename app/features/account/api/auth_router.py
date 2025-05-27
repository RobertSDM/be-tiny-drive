from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from app.database.client.sqlalchemy_client import db_client
from app.core.schemas import AccountResponse
from app.features.account.services.account_serv import account_get_serv
from app.middlewares.auth_middleware import auth_middleware

account_router = APIRouter(dependencies=[Depends(auth_middleware)])


@account_router.get("/{id}")
def account_get(id: str, db: Session = Depends(db_client.get_session)):
    account = account_get_serv(db, id)
    return ORJSONResponse(AccountResponse(data=account).model_dump())
