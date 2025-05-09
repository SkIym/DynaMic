from geopy.distance import great_circle
from sqlmodel import Session, select
from models.survey_group import Survey_Group
from schemas.occurrence import OccurrenceDisplay
from models.buoy import Buoy
from services.occurrence import to_display

def find_survey_group(session: Session, buoy_lat: float, buoy_long: float) -> int | None:
    with session:

        survey_groups = session.exec(select(Survey_Group))
        buoy_point = (buoy_lat, buoy_long)
            
        for group in survey_groups:
            group_point = (group.latitude, group.longitude)
            distance = great_circle(buoy_point, group_point).km
            
            print(distance, group.name)
            if distance <= group.radius:    
                return group.id
        
        return None
    
async def get_occurrences_per_group(id: int, session: Session) -> list[OccurrenceDisplay]:
    with session:

        query = select(Buoy).where(Buoy.group_id == id)
        results = session.exec(query)
        buoys = results.all()

        occurrences: list[OccurrenceDisplay] = []
        for buoy in buoys:
            occurrences.extend(to_display(buoy.occurrences))
        
        return occurrences