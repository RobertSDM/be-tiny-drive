import io
import zipfile

from utils.convert_data import get_base64_to_bytes_data
from database.schemas import FolderSchema


def get_folder_zip(folder: FolderSchema, path: str = "") -> io.BytesIO:

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip:
        for file in folder.files:
            base64Data = file.fileData.byteData
            byteData = get_base64_to_bytes_data(base64Data)  # return io.BytesIO
            full_path = (
                path + file.name + (f".{file.extension}" if file.extension else "")
            )
            zip.writestr(full_path, byteData.getbuffer())

        for subfolder in folder.folders:
            subfolder_path = path + subfolder.name + "/"

            # Cria uma entrada para o diretório vazio
            zip.writestr(subfolder_path, "")

            subfolder_buffer = get_folder_zip(subfolder, subfolder_path)
            subfolder_zip = zipfile.ZipFile(subfolder_buffer)

            for name in subfolder_zip.namelist():
                zip.writestr(name, subfolder_zip.read(name))

            subfolder_zip.close()

    buffer.seek(0)
    return buffer
