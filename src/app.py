from fastapi import FastAPI
from .db import engine, SQLModel
from .routers import buoy

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

app.include_router(buoy.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# if __name__ == "__main__":
#     create_db_and_tables()

