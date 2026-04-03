from fastapi import APIRouter, Body, Query

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only, PaginationDep
from app.schemas.bookings import BookingCreateRequest, BookingFullResponse, MyBookingsResponse
from app.services.bookings import BookingService
from app.core.dependencies import CurrentUser
router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.post("", summary="Создать новую бронь", response_model=BookingFullResponse)
async def create_booking(
        db: DBDep,
        user: CurrentUser,
        payload: BookingCreateRequest,
):
    return await BookingService(db).create_booking(user_id=user.id, payload=payload)

@router.get("/my", summary="Получить мои бронирования", response_model=list[MyBookingsResponse])
async def get_my_bookings(
        db: DBDep,
        user: CurrentUser
):
    return await BookingService(db).get_my_bookings(user_id=user.id)