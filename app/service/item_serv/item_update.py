from sqlalchemy.orm import Session

from app.core.exceptions import ItemNotFound
from app.database.models.item_model import Item
from app.database.repositories.item_repo import item_by_id_ownerid
from app.utils.execute_query import execute_first, update_entity


def item_update_name(db: Session, id: str, ownerid: str, name: str) -> Item:
    query = item_by_id_ownerid(db, id, ownerid)
    item = execute_first(query)
    if not item:
        raise ItemNotFound()

    update_entity(query, {Item.name: name})
    db.commit()
    return item
