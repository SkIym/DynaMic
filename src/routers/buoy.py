from fastapi import APIRouter
from schemas.buoy import BuoyRegister

router = APIRouter(
    prefix="/buoy",
    tags=["buoy"]
)

# Post buoy or register (latitude, longitude, id,)
@router.post("/")
async def register_buoy(buoy: BuoyRegister):
    return buoy