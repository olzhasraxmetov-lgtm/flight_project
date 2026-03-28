from pydantic import BaseModel
from decimal import Decimal

from app.helpers.cabin_class import CabinClass
from app.helpers.seat_status import SeatStatus
from app.helpers.seat_type import SeatType


class SeatInstanceMapResponse(BaseModel):
    id: int
    flight_instance_id: int
    seat_number: str
    row_number: int
    seat_letter: str
    cabin_class: CabinClass
    seat_type: SeatType
    status: SeatStatus
    price_override: Decimal | None = None

class SeatMapShortResponse(BaseModel):
    id: int
    no: str
    cabin_class: CabinClass
    seat_type: SeatType
    status: SeatStatus
    price_override: Decimal | None = None

class FlightInstanceMapResponse(BaseModel):
    flight_instance_id: int
    total_seats: int
    rows: dict[str, list[SeatMapShortResponse]]