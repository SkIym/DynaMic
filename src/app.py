from fastapi import FastAPI, Request
from db import create_db_and_tables
from routers import buoy, survey_group, occurrence
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

app.include_router(buoy.router)
app.include_router(survey_group.router)
app.include_router(occurrence.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
