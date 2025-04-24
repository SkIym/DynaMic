from pydantic import BaseModel

class OccurrenceCreate(BaseModel):
    latitude: float
    longitude: float
