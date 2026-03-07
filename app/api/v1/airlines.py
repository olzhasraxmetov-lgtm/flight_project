from fastapi import APIRouter, Body, Response

from app.core.dependencies import CurrentUser
from app.core.dependencies import DBDep
from app.schemas.airlines import AirlineResponse, AirlineCreate, AirlineUpdate
from app.services.airlines import AirlinesService

router = APIRouter(
    prefix="/airlines",
    tags=["Авиакомпаний"]
)

@router.get("/", response_model=AirlineResponse)
async def get_airlines(

):
    pass