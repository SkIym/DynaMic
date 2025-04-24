from fastapi import APIRouter
from schemas.survey_group import SurveyGroupRegister

router = APIRouter(
    prefix="/sgroup",
    tags=["sgroup"]
)

# Post buoy or register (latitude, longitude, id,)
@router.post("/")
async def register_group(group: SurveyGroupRegister):
    return group