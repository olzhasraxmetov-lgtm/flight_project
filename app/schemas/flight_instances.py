from datetime import datetime

from pydantic import BaseModel, Field, model_validator
from decimal import Decimal

from app.exceptions.api import InvalidDateTimeException
from app.helpers.flight_status import FlightStatus
from app.schemas.airports import AirportShort
from app.schemas.flights import DateParseMixin


class FlightInstanceBase(BaseModel):
    flight_number: str = Field(...)
    base_price: Decimal = Field(..., gt=0, decimal_places=2)
    departure_at: datetime
    arrival_at: datetime
    status: FlightStatus = FlightStatus.SCHEDULED


class FlightInstanceCreate(DateParseMixin, FlightInstanceBase):
    departure_airport_id: int
    arrival_airport_id: int
    seat_template_id: int

    @model_validator(mode="after")
    def validate_arrival_time(self):
        if self.arrival_at <= self.departure_at:
            raise InvalidDateTimeException
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "flight_number": "KC-801",
                "base_price": 45000.00,
                "departure_at": "27.03.2026 15:00",
                "arrival_at": "27.03.2026 18:30",
                "departure_airport_id": 1,
                "arrival_airport_id": 4,
                "seat_template_id": 1
            }
        }
    }


class FlightInstanceResponse(FlightInstanceBase):
    id: int
    departure_airport: AirportShort
    arrival_airport: AirportShort

class FlightInstanceStatusUpdate(BaseModel):
    status: FlightStatus