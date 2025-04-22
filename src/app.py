from fastapi import FastAPI
from db import engine, SQLModel

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    create_db_and_tables()

