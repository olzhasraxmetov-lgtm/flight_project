import pytest

from app.schemas.airports import AirportCreate


@pytest.mark.parametrize(
    "filters, offset, limit, expected_count", [
        ({"country__ilike": "Kazakh"}, 0, 10, 3),

        ({"name": "Almaty International"}, 0, 10, 1),

        ({"city": "Astana"}, 0, 10, 1),

        ({"name": "wrong_name", "country": "Kazakhstan"}, 0, 10, 0),

        ({}, 2, 10, 2)
    ]
)
async def test_get_airports_with_pagination(
        db, filters, offset, limit, expected_count
):
    airports = [
        AirportCreate(
            name="Almaty International",
            code='ALA',
            country="Kazakhstan",
            city="Almaty",
            timezone="Asia/Almaty",
        ),
        AirportCreate(
            code="NQZ",
            name="Nursultan Nazarbayev",
            city="Astana",
            country="Kazakhstan",
            timezone="Asia/Almaty",
        ),
        AirportCreate(
            code="SCO",
            name="Aktau International",
            city="Aktau",
            country="Kazakhstan",
            timezone="Asia/Almaty",
        ),
        AirportCreate(
            code="LHR",
            name="London Heathrow",
            city="London",
            country="United Kingdom",
            timezone="Europe/London",
        )
    ]

    await db.airports.add_bulk(airports)
    await db.commit()

    db_airports = await db.airports.get_paginated_items(
        offset=offset,
        limit=limit,
        **filters

    )
    assert len(db_airports) == expected_count



async def test_add_new_airport(db):
    new_airport = AirportCreate(
        name="Almaty International",
        code='ALA',
        country="Kazakhstan",
        city="Almaty",
        timezone="Asia/Almaty",
    )
    created_airport_db = await db.airports.add(new_airport)
    await db.commit()
    db_airport = await db.airports.get_one(id=created_airport_db.id)

    assert db_airport is not None
    assert db_airport.name == new_airport.name
    assert db_airport.city == new_airport.city
    assert db_airport.country == new_airport.country
    assert db_airport.id is not None

async def test_delete_new_airport(db, created_airport):
    await db.airports.delete(id=created_airport.id)
    await db.commit()

    db_airport = await db.airports.get_one_or_none(id=created_airport.id)
    assert db_airport is None

async def test_get_airport_by_id(db, created_airport):
    airline_db = await db.airports.get_one_or_none(id=created_airport.id)
    assert airline_db
    assert airline_db.name == created_airport.name
    assert airline_db.city == created_airport.city
    assert airline_db.country == created_airport.country

async def test_update_new_airport(db, created_airport):
    new_updated_data = {
        "code": "SCO",
        "name": "Aktau International",
        "city": "Aktau",
        "country": "Kazakhstan",
        "timezone": "Asia/Almaty",
    }
    updated_airport = await db.airports.edit(
        data=new_updated_data,
        id=created_airport.id,
    )
    await db.commit()
    updated_airport_db = await db.airports.get_one(id=updated_airport.id)
    assert updated_airport_db is not None
    assert updated_airport_db.name == new_updated_data["name"]
    assert updated_airport_db.code == new_updated_data["code"]
    assert updated_airport_db.timezone == new_updated_data["timezone"]