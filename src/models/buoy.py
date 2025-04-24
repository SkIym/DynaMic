from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .occurence import Occurrence
    from .survey_group import SurveyGroup
class Buoy(SQLModel, table=True):
    id: int = Field(primary_key=True, description="Id of the device")
    deployed_latitude: float = Field(..., description="Latitude of the occurence")
    deployed_longitude: float = Field(..., description="Longitude of the occurence")
    deployed_at: datetime = Field(default=datetime.now(), nullable=False)
    group_id: int = Field(foreign_key="survey_group.id", description="Id of the surveillance group the buoy belongs to")
    survey_group: "SurveyGroup" = Relationship(back_populates="buoys")
    occurrences: List["Occurrence"] = Relationship(back_populates="buoy")
