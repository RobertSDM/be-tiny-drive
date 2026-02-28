from sqlalchemy.orm import Session

from server.app.core.exceptions import InvalidFileName
from server.app.features.file.utils import get_file_or_raise, verify_name_duplicated
from server.app.utils.utils import validate_filename
from server.app.database.models.FileModel import FileModel


class FileUpdateService:
    def update_filename(
        self, db: Session, id: str, ownerid: str, name: str
    ) -> FileModel:
        if not validate_filename(name):
            raise InvalidFileName(name)

        file = get_file_or_raise(db, ownerid, id, None)

        verify_name_duplicated(
            db, ownerid, file.parentid, name + file.extension, file.is_dir
        )

        file.filename = name
        db.flush()

        return file
