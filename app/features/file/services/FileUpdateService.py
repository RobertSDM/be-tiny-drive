from sqlalchemy.orm import Session

from app.core.validation_errors import InvalidFileName
from app.features.file.utils import get_file_or_raise, verify_name_duplicated
from app.utils.utils import validate_filename
from app.database.models.FileModel import FileModel


class FileUpdateService:
    def update_filename(
        self, db: Session, id: str, ownerid: str, name: str
    ) -> FileModel:
        if not validate_filename(name):
            raise InvalidFileName(name)

        file = get_file_or_raise(db, ownerid, id, None)

        verify_name_duplicated(
            db, ownerid, file.parentid, name + "." + file.extension, file.type
        )

        file.filename = name
        db.flush()

        return file
