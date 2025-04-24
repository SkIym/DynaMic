from fastapi import FastAPI
from db import create_db_and_tables
from routers import buoy


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

app.include_router(buoy.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
