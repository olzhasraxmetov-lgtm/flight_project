from datetime import datetime
from decimal import Decimal

import pytest
from app.schemas.airlines import AirlineCreate
from app.schemas.airports import AirportCreate
from app.schemas.flights import FlightCreate

@pytest.fixture
async def seed_data(db):
    ala = await db.airports.add({
        "code": "ALA", "name": "Almaty", "city": "Almaty",
        "country": "Kazakhstan", "timezone": "Asia/Almaty"
    }, map_res=False)

    nqz = await db.airports.add({
        "code": "NQZ", "name": "Astana", "city": "Astana",
        "country": "Kazakhstan", "timezone": "Asia/Almaty"
    }, map_res=False)

    airline = await db.airlines.add({
        "name": "Fly Arystan", "iata_code": "FC"
    }, map_res=False)

    await db.commit()

    return {
        "ala_id": ala.id,
        "nqz_id": nqz.id,
        "airline_id": airline.id
    }

@pytest.fixture
def flight_factory(db, seed_data):
    async def _create_flights(count: int, price_start: int = 10000):
        flights = []
        for i in range(count):
            flight = FlightCreate(
                flight_number=f"TEST-{i}",
                departure_airport_id=seed_data["ala_id"],
                arrival_airport_id=seed_data["nqz_id"],
                airline_id=seed_data["airline_id"],
                departure_at=datetime(year=2026, month=3, day=25, hour=10, minute=10, second=10),
                arrival_at=datetime(year=2026, month=3, day=25, hour=12, minute=10, second=10),
                price=Decimal(price_start + (i * 1000)),
            )
            res = await db.flights.add(flight, map_res=False)
            flights.append(res)
        await db.commit()
        return flights

    return _create_flights

@pytest.fixture
async def created_flight(db):
    dep_airport = await db.airports.add(AirportCreate(
        code="ALA", name="Almaty", city="Almaty", country="KZ", timezone="Asia/Almaty"
    ))
    arr_airport = await db.airports.add(AirportCreate(
        code="NQZ", name="Astana", city="Astana", country="KZ", timezone="Asia/Almaty"
    ))
    airline = await db.airlines.add(AirlineCreate(
        name="Fly Arystan", iata_code="FC"
    ))
    await db.commit()

    flight_data = FlightCreate(
        flight_number="KC-123",
        departure_at=datetime(year=2026, month=3, day=25, hour=10, minute=30, second=0),
        arrival_at=datetime(year=2026, month=3, day=25, hour=18, minute=45, second=0),
        price=Decimal(345000.00),
        departure_airport_id=dep_airport.id,
        arrival_airport_id=arr_airport.id,
        airline_id=airline.id
    )

    flight = await db.flights.add(flight_data, map_res=False)

    await db.commit()

    return flight


@pytest.fixture
async def flight_update_data(db, created_flight):
    new_airport = await db.airports.add(AirportCreate(
        code="SCO", name="Aktau", city="Aktau", country="KZ", timezone="Asia/Almaty"
    ))

    new_airline = await db.airlines.add(AirlineCreate(
        name="Qazaq Air", iata_code="IQ"
    ))

    await db.commit()

    return {
        "flight": created_flight,
        "new_airport_id": new_airport.id,
        "new_airline_id": new_airline.id
    }


