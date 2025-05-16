from fastapi import FastAPI, Request
from db import create_db_and_tables
from routers import buoy, survey_group, occurrence, ws
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from routers.survey_group import get_all_groups

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}}, lifespan=lifespan)

app.mount("/static", StaticFiles(directory="../static"), name="static")

templates = Jinja2Templates(directory="../templates")

app.include_router(buoy.router)
app.include_router(survey_group.router)
app.include_router(occurrence.router)
app.include_router(ws.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    groups = await get_all_groups()
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={
            "groups": groups
        }
    )


