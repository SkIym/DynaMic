from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .buoy import Buoy
class Occurrence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    latitude: float = Field(..., description="Latitude of the occurence")
    longitude: float = Field(..., description="Longitude of the occurence")
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    buoy_id: int = Field(..., description="Id of the detecting buoy", foreign_key="buoy.id")
    buoy: "Buoy" = Relationship(back_populates="occurrences")


