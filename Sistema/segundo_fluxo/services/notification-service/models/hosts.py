
from pydantic import BaseModel


class Hosts(BaseModel):
    url: str
    chat_id: str