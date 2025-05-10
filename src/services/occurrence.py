from models.occurrence import Occurrence
from schemas.occurrence import OccurrenceDisplay
from typing import Sequence
from models.buoy import Buoy
from datetime import datetime
from sqlmodel import Session, select

def to_display(occs: Sequence[Occurrence]) -> list[OccurrenceDisplay]:
    
    formatted_occs = map(
        lambda occ: OccurrenceDisplay(
            date=occ.created_at.strftime("%A, %B %d %Y"),
            time=occ.created_at.strftime("%I:%M:%S %p"),
            latitude=occ.latitude,
            longitude=occ.longitude
        ),
        occs
    )
    return list(formatted_occs)

async def get_occurrences_per_group(start_date: datetime, id: int, session: Session) -> list[OccurrenceDisplay]:
    with session:

        query = select(Occurrence).join(Buoy).where(Buoy.group_id == id).where(Occurrence.created_at > start_date)
        results = session.exec(query)
        occurrences = results.all()
        return to_display(occurrences)