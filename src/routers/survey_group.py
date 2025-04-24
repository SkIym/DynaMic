from fastapi import APIRouter
from schemas.survey_group import SurveyGroupRegister
from sqlmodel import Session
from db import engine
from models.survey_group import Survey_Group

router = APIRouter(
    prefix="/sgroup",
    tags=["sgroup"]
)

# Register a group (latitude, longitude, name, radius)
@router.post("/", response_model=Survey_Group)
async def register_group(group: SurveyGroupRegister):

    new_group = Survey_Group(**group.model_dump())

    with Session(engine) as session:
        session.add(new_group)
        session.commit()
        session.refresh(new_group)
        return new_group