# from sqlalchemy.orm import Session

# from app.core.exceptions import NotFound
# from app.core.validation_errors import InvalidFileName
# from app.utils.utils import validate_filename
# from app.database.models.file_model import File
# from app.database.repositories.item_repo import file_by_id_ownerid
# from app.features.file.services.item_checks import item_checks
# from app.utils.query import exec_first


# class _ItemUpdateServ:
#     def item_update_name(self, db: Session, id: str, ownerid: str, name: str) -> File:
#         if not validate_filename(name):
#             raise InvalidFileName(name)

#         item = exec_first(file_by_id_ownerid(db, id, ownerid))

#         if not item:
#             raise NotFound()

#         item_checks.check_duplicate_name(
#             db, ownerid, item.parentid, name + item.extension, item.type
#         )

#         item.filename = name
#         db.commit()
#         return item


# item_update_serv = _ItemUpdateServ()
