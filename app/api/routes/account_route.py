from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.orm import Session
from app.clients.sqlalchemy_client import db_client
from app.core.schemas import AccountResponse
from app.service.account_serv import account_get_serv

account_router = APIRouter()


@account_router.get("/{id}")
def account_get(id: str, db: Session = Depends(db_client.get_session)):
    account = account_get_serv(db, id)
    return ORJSONResponse(AccountResponse(data=account).model_dump())
