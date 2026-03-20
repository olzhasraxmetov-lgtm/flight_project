from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator
from decimal import Decimal

from app.exceptions.api import InvalidDateTimeException
from app.exceptions.base import SameAirportException
from app.schemas.airports import AirportShort
from app.schemas.airlines import AirlineShort

class DateParseMixin:
    @field_validator("departure_at", "arrival_at", mode="before")
    @classmethod
    def parse_datetime(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value
        formats = [
            "%d.%m.%Y %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                continue

        return value

class FlightBase(BaseModel):
    flight_number: str = Field(min_length=4, max_length=12,description="Номер рейса")
    departure_at: datetime = Field(json_schema_extra={"default-example-departure": "15.03.2026 10:00"},description="Время вылета рейса")
    arrival_at: datetime = Field(json_schema_extra={"default-example-arrival": "15.03.2026 14:30"},description="Время прилета рейса")
    price: Decimal = Field(default=Decimal('0.00'), ge=0,description="Цена рейса")

class FlightUpdate(DateParseMixin, BaseModel):
    flight_number: str | None = Field(None,min_length=4, max_length=12)
    departure_at: datetime | None = Field(default=None,json_schema_extra={"default_example_departure": "15.03.2026 10:00"})
    arrival_at: datetime  | None= Field(default=None,json_schema_extra={"default_example_arrival": "15.03.2026 14:30"})
    price: Decimal | None = Field(None, ge=0)

    departure_airport_id: int | None = Field(default=None)
    arrival_airport_id: int | None = Field(default=None)
    airline_id: int | None = Field(default=None)

class FlightResponseWithoutRels(FlightBase):
    id: int
    departure_airport_id: int
    arrival_airport_id: int
    airline_id: int

class FlightCreate(DateParseMixin, FlightBase):
    departure_airport_id: int
    arrival_airport_id: int
    airline_id: int


class FlightResponse(FlightBase):
    id: int

    departure_airport: AirportShort
    arrival_airport: AirportShort
    airline: AirlineShort

class FlightSearch(BaseModel):
    departure_airport_id: int | None = Field(default=None)
    arrival_airport_id: int | None = Field(default=None)
    airline_id: int | None = Field(default=None)
    date_from: datetime | None = Field(default=None)
    date_to: datetime | None = Field(default=None)
    max_price: Decimal | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def parse_airports_data(self):
        if (self.departure_airport_id is not None and
                self.arrival_airport_id is not None and
                self.departure_airport_id == self.arrival_airport_id):
            raise SameAirportException

        if self.date_from and self.date_to:
            if self.date_from >= self.date_to:
                raise InvalidDateTimeException
        return self