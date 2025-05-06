from pydantic import BaseModel

class OccurrenceCreate(BaseModel):
    latitude: float
    longitude: float
    buoy_id: int
class OccurrenceDisplay(BaseModel):
    date: str
    time: str
    latitude: float
    longitude: float
