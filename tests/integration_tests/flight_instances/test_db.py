from sqlalchemy.orm import joinedload

from app.models.flight_instances import FlightInstancesORM
from app.services.flight_instances import FlightInstancesService


async def test_flight_instances_pagination_logic(db, flight_instances_factory):
    instances = await flight_instances_factory(count=5)
    instances.sort(key=lambda x: x.id)

    options = [
        joinedload(FlightInstancesORM.departure_airport),
        joinedload(FlightInstancesORM.arrival_airport),
    ]

    page_1 = await db.flight_instances.get_paginated_items(limit=2, offset=0, options=options)
    assert len(page_1) == 2
    assert page_1[0].id == instances[0].id
    assert page_1[1].id == instances[1].id

    page_2 = await db.flight_instances.get_paginated_items(limit=2, offset=2, options=options)
    assert len(page_2) == 2
    assert page_2[0].id == instances[2].id
    assert page_2[1].id == instances[3].id

    page_empty = await db.flight_instances.get_paginated_items(limit=10, offset=100, options=options)
    assert len(page_empty) == 0


async def test_create_flight_instance(db, created_flight_instance):
    db_flight = await db.flight_instances.get_one_with_details(flight_instance_id=created_flight_instance.id)
    assert db_flight is not None
    assert db_flight.id is not None


async def test_get_flight_instance_map(db, created_flight_instance):
    service = FlightInstancesService(db)

    response = await service.get_flight_instance_map(created_flight_instance.id)
    assert response.total_seats > 0
    assert len(response.rows) > 0
    first_row_key = list(response.rows.keys())[0]
    first_row_seats = response.rows[first_row_key]
    sample_seat = first_row_seats[0]
    hasattr(sample_seat, 'id')
    hasattr(sample_seat, 'status')
    isinstance(sample_seat.no, str)

async def test_update_flight_instance_status(db, created_flight_instance):
    updated_flight_instance = await db.flight_instances.edit(data={"status": "cancelled"}, map_res=False)
    db_flight = await db.flight_instances.get_one_with_details(flight_instance_id=updated_flight_instance.id)

    assert created_flight_instance.status != db_flight.status