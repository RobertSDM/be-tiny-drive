from sqlalchemy.orm import Session

from app.core.exceptions import ItemNotFound
from app.core.validation_errors import InvalidItemName
from app.core.validations import validate_item_name
from app.database.models.item_model import Item
from app.database.repositories.item_repo import item_by_id_ownerid
from app.features.items.services.item_checks import item_checks
from app.utils.query import exec_first, update


class _ItemUpdateServ:
    def item_update_name(self, db: Session, id: str, ownerid: str, name: str) -> Item:
        if not validate_item_name(name):
            raise InvalidItemName(name)

        item = exec_first(item_by_id_ownerid(db, id, ownerid))

        if not item:
            raise ItemNotFound()

        item_checks.check_duplicate_name(
            db, ownerid, item.parentid, name + item.extension, item.type
        )

        item.name = name
        db.commit()
        return item


item_update_serv = _ItemUpdateServ()
