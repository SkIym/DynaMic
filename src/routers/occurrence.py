from fastapi import APIRouter, HTTPException
from schemas.occurrence import OccurrenceCreate, OccurrenceDisplay
from models.occurrence import Occurrence
from sqlmodel import Session, select
from db import engine
from services.buoy import registered_buoy
from services.occurrence import to_display
from datetime import datetime

router = APIRouter(
    prefix="/occurrences",
    tags=["occurrence"]
)

# Register an explosion (latitude, longitude, id,)
@router.post("/{buoy_id}", response_model=Occurrence)
async def register_explosion(
    buoy_id: int,
    occ: OccurrenceCreate):
    with Session(engine) as session:

        if not registered_buoy(session, buoy_id):
            raise HTTPException(
                status_code=400,
                detail="Device is not yet registered in the system"
            )

        new_occur = Occurrence(
            **occ.model_dump(),
            created_at=datetime.now(),
            buoy_id=buoy_id
        )

        session.add(new_occur)
        session.commit()
        session.refresh(new_occur)
        return new_occur
    
@router.get("", response_model=list[OccurrenceDisplay])
async def get_all_occurrences():
    with Session(engine) as session:
        query = select(Occurrence)
        results = session.exec(query)
        occurrences = results.all()

        return to_display(occurrences)

    