from typing import Optional
from pydantic import BaseModel
from deta import Deta

deta = Deta()
db = deta.Base("change_detector")

class WatchForm(BaseModel):
    name: str
    url: str
    xpath: str

class Watch(WatchForm):
    key: Optional[str]
    created_time: float
    # last triggered time
    updated_time: float
    # each element is (timestamp, value) tuple
    values: list[tuple[float, Optional[str]]]