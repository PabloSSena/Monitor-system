from pydantic import BaseModel

class MonitorRequest(BaseModel):
    cmd: str
    host: str
    interval: int = 5

class MonitorStatus(BaseModel):
    host: str
    tcp: bool