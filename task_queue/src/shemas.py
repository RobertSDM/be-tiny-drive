from pydantic import BaseModel


class PreviewBody(BaseModel):
    fileid: str
    content_type: str
    ownerid: str
