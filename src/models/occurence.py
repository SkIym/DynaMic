from datetime import datetime
from sqlmodel import Field, SQLModel
class Occurrence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    latitude: float = Field(..., description="Latitude of the occurence")
    longitude: float = Field(..., description="Longitude of the occurence")
    buoy_id: int = Field(..., description="Id of the detecting buoy", foreign_key="buoy.id")
    created_at: datetime = Field(default=datetime.now(), nullable=False, primary_key=True)
