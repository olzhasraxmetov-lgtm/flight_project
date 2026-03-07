from fastapi import APIRouter, Body, Response

from app.core.dependencies import CurrentUser, admin_only
from app.core.dependencies import DBDep
from app.schemas.airlines import AirlineResponse, AirlineCreate, AirlineUpdate
from app.services.airlines import AirlinesService

router = APIRouter(
    prefix="/airlines",
    tags=["Авиакомпаний"]
)

@router.get("/", response_model=list[AirlineResponse], summary='Получит список авиакомпаний')
async def get_airlines(

):
    pass


@router.get("/{airline_id}", summary='Получить авиакомпанию по ID')
async def get_airline(

):
    pass

@router.post("/", summary='Добавить новую авиакомпанию', dependencies=[admin_only])
async def create_airline(
    db: DBDep,
    payload: AirlineCreate = Body(...),
):
    return await AirlinesService(db).create_airline(payload=payload)



@router.put("/", summary='Обновить авиакомпанию', dependencies=[admin_only])
async def update_airlines(

):
    pass

@router.patch("/", summary='Частично обновить авиакомпанию', dependencies=[admin_only])
async def update_airlines(

):
    pass

@router.delete("/", summary='Удалить авиакомпанию', dependencies=[admin_only])
async def delete_airlines(

):
    pass