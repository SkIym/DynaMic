from fastapi import APIRouter
from schemas.buoy import BuoyRegister
from models.buoy import Buoy
from sqlmodel import Session
from db import engine

router = APIRouter(
    prefix="/buoy",
    tags=["buoy"]
)

# Register a buoy (latitude, longitude, id,)
@router.post("/create")
async def register_buoy(buoy: BuoyRegister):
    with Session(engine) as session:
        new_buoy = Buoy(**buoy.model_dump())

        lat = new_buoy.deployed_latitude
        long = new_buoy.deployed_longitude

        session.add(new_buoy)
        session.commit()
        session.refresh(new_buoy)
        return new_buoy
    


    