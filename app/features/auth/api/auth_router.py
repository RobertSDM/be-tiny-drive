from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from app.database.client.sqlalchemy_client import db_client
from sqlalchemy.orm import Session

from app.core.schemas import AuthRegisterResponse
from app.features.auth.services.auth_serv import register_serv

auth_router = APIRouter()


class RegisterBody(BaseModel):
    username: str
    email: str
    password: str


@auth_router.post("/register")
def register(body: RegisterBody, db: Session = Depends(db_client.get_session)):
    account = register_serv(db, body.username, body.email, body.password)

    return ORJSONResponse(AuthRegisterResponse(data=account).model_dump())
