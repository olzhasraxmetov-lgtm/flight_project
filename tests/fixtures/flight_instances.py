from datetime import datetime
from decimal import Decimal

import pytest

from app.helpers.flight_status import FlightStatus
from app.helpers.seat_status import SeatStatus
from app.schemas.flight_instances import FlightInstanceCreate


@pytest.fixture
async def created_flight_instance(db, seed_data, created_seat_templates_seats, created_seat_template):
    flight_data = FlightInstanceCreate(
        flight_number="KC-851",
        departure_at=datetime(year=2026, month=3, day=25, hour=10, minute=30, second=0),
        arrival_at=datetime(year=2026, month=3, day=25, hour=18, minute=45, second=0),
        base_price=Decimal(345000.00),
        departure_airport_id=seed_data["ala_id"],
        arrival_airport_id=seed_data["nqz_id"],
        seat_template_id=created_seat_template.id,
        status=FlightStatus.SCHEDULED
    )

    flight_instance = await db.flight_instances.add(flight_data, map_res=False)
    await db.session.flush()
    await db.session.refresh(flight_instance)

    template_seats = await db.seat_template_seats.get_all(
        seat_template_id=created_seat_template.id
    )
    seats_to_create = [
        {
            "flight_instance_id": flight_instance.id,
            "seat_number": s.seat_number,
            "row_number": s.row_number,
            "seat_letter": s.seat_letter,
            "cabin_class": s.cabin_class,
            "seat_type": s.seat_type,
            "status": SeatStatus.AVAILABLE
        }
        for s in template_seats
    ]
    if seats_to_create:
        await db.seat_instances_map.add_bulk(seats_to_create)

    await db.session.commit()
    return await db.flight_instances.get_one_with_details(flight_instance.id)

@pytest.fixture
def flight_instances_factory(db, seed_data, created_seat_template):
    async def _create_flights(count: int, price_start: int = 30000):
        flights = []
        for i in range(count):
            flight = FlightInstanceCreate(
                flight_number=f"TEST-{i}",
                departure_airport_id=seed_data["ala_id"],
                arrival_airport_id=seed_data["nqz_id"],
                seat_template_id=created_seat_template.id,
                departure_at=datetime(year=2026, month=3, day=25, hour=10, minute=10, second=10),
                arrival_at=datetime(year=2026, month=3, day=25, hour=12, minute=10, second=10),
                base_price=Decimal(price_start + (i * 1000)),
            )
            res = await db.flight_instances.add(flight, map_res=False)
            flights.append(res)
        await db.commit()
        return flights

    return _create_flights
