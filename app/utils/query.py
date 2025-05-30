from typing import TypeVar
from sqlalchemy.orm import Session, Query, InstrumentedAttribute

from app.database.models.item_model import Item
from app.enums.enums import Sort, SortOrder

T = TypeVar("T")

def order_by(query: Query[T], columns: list[InstrumentedAttribute], order: SortOrder):
    match order:
        case SortOrder.ASC:
            return query.order_by(*(col.asc() for col in columns))
        case SortOrder.DESC:
            return query.order_by(*(col.desc() for col in columns))


def select_order_item_column(type: Sort) -> InstrumentedAttribute:
    match type:
        case Sort.NAME:
            return Item.name
        case Sort.UPDATE_DATE:
            return Item.update_date


def paginate(query: Query[T], limit: int, page: int) -> Query[T]:
    return query.limit(limit).offset(page * limit)


def update(query: Query[T], data: dict[any, any]) -> None:
    query.update(data)


def exec_all(query: Query[T]) -> list[T]:
    return query.all()


def exec_first(query: Query[T]) -> T | None:
    return query.first()


def exec_exists(db: Session, query: Query[T]) -> bool:
    return db.query(query.exists()).scalar()
