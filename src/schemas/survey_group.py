from pydantic import BaseModel

class SurveyGroupRegister(BaseModel):
    name: str 
    latitude: float
    longitude: float
    radius: float
