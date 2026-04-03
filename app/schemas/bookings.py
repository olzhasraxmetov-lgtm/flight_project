from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, AliasPath

from app.helpers.booking_status import BookingStatus


class PassengerCreate(BaseModel):
    first_name: str = Field(min_length=3, max_length=10)
    last_name: str= Field(min_length=3, max_length=40)
    passport_number: str = Field(..., pattern=r"^[a-zA-Z0-9]{6,9}$")
    seat_instance_id: int


class BookingCreateRequest(BaseModel):
    flight_instance_id: int
    passengers: list[PassengerCreate]

class PassengerInternalCreateRequest(PassengerCreate):
    booking_id: int
    flight_instance_id: int
    price: Decimal

class PassengerShortResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    passport_number: str
    seat_instance_id: int
    price: Decimal

class BookingInternalCreate(BaseModel):
    user_id: int
    booking_reference: str
    total_price: Decimal
    status: BookingStatus = BookingStatus.CREATED

class FlightBriefResponse(BaseModel):
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_at: datetime

class BookingFullResponse(BaseModel):
    id: int
    user_id: int
    flight_number: str = Field(
        validation_alias=AliasPath("passengers", 0, "flight_instance", "flight_number"),
    )
    departure_at: datetime = Field(
        validation_alias=AliasPath("passengers", 0, "flight_instance", "departure_at")
    )
    arrival_at: datetime = Field(
        validation_alias=AliasPath("passengers", 0, "flight_instance", "arrival_at")
    )
    booking_reference: str
    total_price: Decimal
    status: BookingStatus

    passengers: list[PassengerShortResponse]

    created_at: datetime


class MyBookingsResponse(BaseModel):
    id: int
    booking_reference: str
    flight_number: str | None = None
    departure_at: datetime | None = None
    arrival_at: datetime | None = None

    total_price: Decimal
    status: BookingStatus

    passengers_count: int = 0

    created_at: datetime