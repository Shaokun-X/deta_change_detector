from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from action import router as action_router
from model import db, Watch, WatchForm
from utils import fetch_all_watches, execute_watch


def latest_value(values: list[tuple[float, Optional[str]]]) -> Optional[str]:
    if values:
        values.sort(key=lambda v: v[0])
        return values[-1][1]

def latest_update_time(values: list[tuple[float, Optional[str]]]) -> datetime:
    if values:
        values.sort(key=lambda v: v[0])
        return datetime.fromtimestamp(values[-1][0])

templates = Jinja2Templates(directory="templates")
templates.env.filters = {"latest_value": latest_value, "latest_update_time": latest_update_time}

app = FastAPI()
app.include_router(action_router)

@app.get("/")
def index(request: Request):
    items = fetch_all_watches()
    return templates.TemplateResponse("index.jinja", {"request": request, "items": items})

@app.get("/list")
def list_(request: Request):
    items = fetch_all_watches()
    return templates.TemplateResponse("_list.jinja", {"request": request, "items": items})

@app.post("/")
def create(request: Request, data: WatchForm):
    watch = Watch(
        **data.model_dump(),
        created_time=datetime.utcnow().timestamp(),
        updated_time=datetime.utcnow().timestamp(),
        values=[],
        key=None
    )
    db.put(watch.model_dump())
    execute_watch(watch)
    items = fetch_all_watches()
    return templates.TemplateResponse("_list.jinja", {"request": request, "items": items})

@app.post("/{key}")
def check(request: Request, key: str):
    result = db.get(key)
    if result:
        item = Watch(**result)
        execute_watch(item)
        return templates.TemplateResponse("_item.jinja", {"request": request, "item": item})
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Item not found")

@app.get("/edit/{key}")
def update_snippet(request: Request, key: str):
    result = db.get(key)
    if result:
        item = Watch(**result)
        return templates.TemplateResponse("_edit.jinja", {"request": request, "item": item})
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Item not found")
    
@app.put("/{key}")
def update(request: Request, key: str, data: WatchForm):
    if db.get(key):
        db.update({
            **data.model_dump(),
            "updated_time": datetime.utcnow().timestamp()
        }, key)
        item = Watch(**db.get(key))
        return templates.TemplateResponse("_item.jinja", {"request": request, "item": item})
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete("/{key}")
def delete(key: str):
    db.delete(key)
    return Response(status_code=HTTP_200_OK)
