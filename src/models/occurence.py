from typing import Annotated
from datetime import datetime, UTC
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Occurence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    latitude: float = Field(..., description="Latitude of the occurence")
    longitude: float = Field(..., description="Longitude of the occurence")
    created_at: datetime = datetime('now')