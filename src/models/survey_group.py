from sqlmodel import Field, SQLModel

class SurveyGroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, description="Name of the surveillance group")
    latitude: float = Field(..., description="Latitude of the occurence")
    longitude: float = Field(..., description="Longitude of the occurence")
    radius: float = Field(..., description="Radius")