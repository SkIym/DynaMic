from pydantic import BaseModel


class BuoyRegister(BaseModel):
    id: int
    deployed_latitude: float
    deployed_longitude: float
