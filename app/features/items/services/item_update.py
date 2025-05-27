from sqlalchemy.orm import Session

from app.core.exceptions import ItemNotFound
from app.database.models.item_model import Item
from app.database.repositories.item_repo import item_by_id_ownerid
from app.utils.query import exec_first, update


class _ItemUpdateServ:
    def item_update_name(self, db: Session, id: str, ownerid: str, name: str) -> Item:
        query = item_by_id_ownerid(db, id, ownerid)
        item = exec_first(query)
        if not item:
            raise ItemNotFound()

        update(query, {Item.name: name})
        db.commit()
        return item


item_update_serv = _ItemUpdateServ()
