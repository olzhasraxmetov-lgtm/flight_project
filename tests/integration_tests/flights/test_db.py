from sqlalchemy.orm import joinedload

from app.models import FlightsORM


async def test_flights_pagination_logic(db, flight_factory):
    await flight_factory(count=15)

    options = [
        joinedload(FlightsORM.departure_airport),
        joinedload(FlightsORM.arrival_airport),
        joinedload(FlightsORM.airline)
    ]

    page_1 = await db.flights.get_paginated_items(limit=10, offset=0, options=options)
    assert len(page_1) == 10

    page_2 = await db.flights.get_paginated_items(limit=10, offset=10, options=options)
    assert len(page_2) == 5

    page_3 = await db.flights.get_paginated_items(limit=10, offset=20, options=options)
    assert len(page_3) == 0


async def test_pagination_page_two(flight_factory, ac):
    await flight_factory(count=15)

    response = await ac.get("/flights", params={"page": 2, "per_page": 10})

    assert len(response.json()) == 5

async def test_create_new_flight(db, created_flight):
    db_flight = await db.flights.get_flight_with_rels(flight_id=created_flight.id)
    assert db_flight is not None
    assert db_flight.id is not None
    
async def test_delete_flight(db, created_flight):
    await db.flights.delete(id=created_flight.id)
    await db.commit()

    db_flight = await db.flights.get_one_or_none(id=created_flight.id)
    assert db_flight is None

async def test_get_flight_by_id(db, created_flight):
    flight_db = await db.flights.get_flight_with_rels(flight_id=created_flight.id)
    assert flight_db
    assert flight_db.flight_number == created_flight.flight_number
    assert flight_db.price == created_flight.price
    assert flight_db.id == created_flight.id

async def test_update_flight(db, flight_update_data):
    flight = flight_update_data["flight"]

    update_payload = {
        "flight_number": "IQ-777",
        "price": 45000,
        "departure_airport_id": flight_update_data["new_airport_id"],
        "airline_id": flight_update_data["new_airline_id"]
    }

    await db.flights.edit(id=flight.id, data=update_payload, map_res=False)
    await db.commit()

    updated = await db.flights.get_flight_with_rels(flight_id=flight.id)

    assert updated.flight_number == "IQ-777"
    assert updated.departure_airport.id == flight_update_data["new_airport_id"]
    assert updated.price == 45000