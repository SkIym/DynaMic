from typing import Annotated
from datetime import datetime, UTC
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, DateTime

class Device(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    deployed_latitude: float = Field(..., description="Latitude of the occurence")
    deployed_longitude: float = Field(..., description="Longitude of the occurence")
    deployed_at: datetime = Field(default=datetime.now(), nullable=False)

class Occurrence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    latitude: float = Field(..., description="Latitude of the occurence")
    longitude: float = Field(..., description="Longitude of the occurence")
    device_id: int = Field(..., description="Id of the detecting buoy", foreign_key="device.id")
    created_at: datetime = Field(default=datetime.now(), nullable=False)
