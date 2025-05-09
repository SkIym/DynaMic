from fastapi import APIRouter, HTTPException
from schemas.occurrence import OccurrenceCreate, OccurrenceDisplay
from models.occurrence import Occurrence
from sqlmodel import Session, select
from db import engine
from services.buoy import registered_buoy
from services.occurrence import to_display
from datetime import datetime
from zoneinfo import ZoneInfo
from services.survey_group import get_occurrences_per_group

router = APIRouter(
    prefix="/occurrences",
    tags=["occurrence"]
)

# Register an explosion (latitude, longitude, id,)
@router.post("", response_model=Occurrence)
async def register_explosion(occ: OccurrenceCreate):
    with Session(engine) as session:

        if not registered_buoy(session, occ.buoy_id):
            raise HTTPException(
                status_code=400,
                detail="Device is not yet registered in the system"
            )

        new_occur = Occurrence(
            **occ.model_dump(),
            created_at=datetime.now(ZoneInfo("Asia/Manila"))
        )

        session.add(new_occur)
        session.commit()
        session.refresh(new_occur)
        return new_occur
    
@router.get("", response_model=list[OccurrenceDisplay])
async def get_occurrences(iso_start_date: str = "", group: int = 0):
    with Session(engine) as session:

        start_date = datetime.fromisoformat(iso_start_date.replace("Z", "+00:00"))
        adjusted_start_date  = start_date.astimezone(ZoneInfo("Asia/Manila"))

        # if specific survey group is selected
        if group:
            occurrences = await get_occurrences_per_group(adjusted_start_date, group, session)
            return occurrences
    
        # get all occurrences
        query = select(Occurrence).where(Occurrence.created_at > adjusted_start_date)
        results = session.exec(query)
        occurrences = results.all()

        return to_display(occurrences)
