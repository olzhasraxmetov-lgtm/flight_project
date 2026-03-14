from fastapi import APIRouter, Query, Depends

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only, PaginationDep

router = APIRouter(
    prefix="/flights",
    tags=["Вылеты"],
)

@router.get('', summary='Получить список вылетов')
async def get_paginated_flights():
    pass

@router.post('', summary='Создать новый вылет', dependencies=[admin_only])
async def create_flight():
    pass
