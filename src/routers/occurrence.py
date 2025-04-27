from fastapi import APIRouter, HTTPException
from schemas.occurrence import OccurrenceCreate
from models.occurrence import Occurrence
from sqlmodel import Session
from db import engine
from services.buoy import registered_buoy

router = APIRouter(
    prefix="/occurrence",
    tags=["occurrence"]
)

# Register an explosion (latitude, longitude, id,)
@router.post("/create/{id}", response_model=Occurrence)
async def register_explosion(
    id: int,
    occ: OccurrenceCreate):
    with Session(engine) as session:

        if not registered_buoy(session, id):
            raise HTTPException(
                status_code=400,
                detail="Device id is not yet registered in the system"
            )

        new_occur = Occurrence(
            **occ.model_dump(),
            buoy_id=id
        )

        session.add(new_occur)
        session.commit()
        session.refresh(new_occur)
        return new_occur
    


    