from pydantic import BaseModel

class SurveyGroupRegister(BaseModel):
    id: int
    name: str 
    latitude: float
    longitude: float
    radius: float
