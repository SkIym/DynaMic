from fastapi import APIRouter, HTTPException
from schemas.buoy import BuoyRegister
from models.buoy import Buoy
from sqlmodel import Session
from db import engine
from services.survey_group import find_survey_group

router = APIRouter(
    prefix="/buoy",
    tags=["buoy"]
)

# Register a buoy (latitude, longitude, id,)
@router.post("/create")
async def register_buoy(buoy: BuoyRegister):
    with Session(engine) as session:

        group_id = find_survey_group(
            session=session,
            buoy_lat=buoy.deployed_latitude,
            buoy_long=buoy.deployed_longitude
        )

        if group_id is None:
            raise HTTPException(
                status_code=404,
                detail="Buoy is not within range of any registered surveillance groups"
            )

        new_buoy = Buoy(
            **buoy.model_dump(),
            group_id=group_id
        )

        session.add(new_buoy)
        session.commit()
        session.refresh(new_buoy)
        return new_buoy
    


    