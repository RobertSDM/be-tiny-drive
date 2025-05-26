from typing import Callable, TypeVar
from sqlalchemy.orm import Session, Query, InstrumentedAttribute

from app.database.models.item_model import Item
from app.enums.enums import Sort, SortOrder

T = TypeVar("T")


def order_by(
    query: Query[T], columns: list[InstrumentedAttribute], sort_order: SortOrder
):
    match sort_order:
        case SortOrder.ASC:
            return query.order_by(columns[0].asc(), *(col.asc() for col in columns[1:]))
        case SortOrder.DESC:
            return query.order_by(
                columns[0].desc(), *(col.desc() for col in columns[1:])
            )


def select_order(type: Sort) -> InstrumentedAttribute:
    match type:
        case Sort.NAME:
            return Item.name
        case Sort.CREATION_DATE:
            return Item.creation_date
        case Sort.UPDATE_DATE:
            return Item.update_date


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
