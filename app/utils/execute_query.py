from typing import TypeVar
from sqlalchemy.orm import Session, Query


T = TypeVar("T")


def update_entity(query: Query[T], data: dict[any, any]) -> None:
    query.update(data)
    

def execute_all(query: Query[T]) -> list[T]:
    return query.all()


def execute_first(query: Query[T]) -> T | None:
    return query.first()


def execute_exists(db: Session, query: Query[T]) -> bool:
    return db.query(query.exists()).scalar()
