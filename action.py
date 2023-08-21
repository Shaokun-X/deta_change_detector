from fastapi import APIRouter
from pydantic import BaseModel

from utils import fetch_all_watches, execute_watch

router = APIRouter()

class ActionEvent(BaseModel):
    id: str
    trigger: str

class Action(BaseModel):
    event: ActionEvent


@router.post("/__space/v0/actions")
def actions(action: Action):
    if action.event.id == "scrape":
        watches = fetch_all_watches()
        for watch in watches:
            execute_watch(watch, notify=True)