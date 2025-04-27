from sqlmodel import Session, select
from models.buoy import Buoy

def registered_buoy(session: Session, buoy_id: int) -> bool:

    with session:
        query = select(Buoy).where(Buoy.id == buoy_id)
        result = session.exec(query)
        buoy = result.first()
        
        if buoy:
            return True
        return False