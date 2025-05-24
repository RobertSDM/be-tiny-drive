from typing import Callable, TypeVar
from sqlalchemy.orm import Session, Query

T = TypeVar("T")


def query_pipe(*funcs: Callable):
    def run(*args, **kwargs):
        result = funcs[0](*args, **kwargs)
        for func in funcs[1:]:
            if result:
                result = func(result)
            else:
                result = func()

        return result

    return run


def paginate(query: Query[T], limit: int, page: int) -> list[T]:
    return query.limit(limit).offset(page * limit)


def update_entity(query: Query[T], data: dict[any, any]) -> None:
    query.update(data)


def execute_all(query: Query[T]) -> list[T]:
    return query.all()


def execute_first(query: Query[T]) -> T | None:
    return query.first()


def execute_exists(db: Session, query: Query[T]) -> bool:
    return db.query(query.exists()).scalar()
