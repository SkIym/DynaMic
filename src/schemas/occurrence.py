from pydantic import BaseModel

class OccurrenceCreate(BaseModel):
    latitude: float
    longitude: float

class OccurrenceDisplay(BaseModel):
    date: str
    time: str
    latitude: float
    longitude: float
