from models.occurrence import Occurrence
from schemas.occurrence import OccurrenceDisplay
from typing import Sequence


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
    