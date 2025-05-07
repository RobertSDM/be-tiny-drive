from typing import TypeVar
from sqlalchemy.orm import Session, Query

from database.models import Item

T = TypeVar("T")


def execute_all(db: Session, query: Query[T]) -> list[T]:
    return query.all()


def execute_first(db: Session, query: Query[T]) -> T:
    return query.first()


def execute_exists(db: Session, query: Query[T]) -> bool:
    return db.query(query.exists()).scalar()
