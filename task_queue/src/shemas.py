from pydantic import BaseModel


class PreviewBody(BaseModel):
    id_: str
    content_type: str
    ownerid: str
