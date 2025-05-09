from fastapi import APIRouter
from schemas.survey_group import SurveyGroupRegister, SurveyGroupDisplay
from sqlmodel import Session, select
from db import engine
from models.survey_group import Survey_Group

router = APIRouter(
    prefix="/survey-groups",
    tags=["survey-group"]
)

# Register a group (latitude, longitude, name, radius)
@router.post("", response_model=Survey_Group)
async def register_group(group: SurveyGroupRegister):
    with Session(engine) as session:
        new_group = Survey_Group(**group.model_dump())
        session.add(new_group)
        session.commit()
        session.refresh(new_group)
        return new_group

@router.get("", response_model=list[SurveyGroupDisplay])
async def get_all_groups():
    with Session(engine) as session:
        query = select(Survey_Group)
        results = session.exec(query)
        groups = results.all()

        return groups

