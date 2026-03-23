from app.schemas.aircrafts import AircraftCreate

async def test_add_new_aircraft(db):
    new_aircraft = AircraftCreate(
        name="A320 Airbus",
        manufacturer="Airbus",
    )
    created_aircraft_db = await db.aircrafts.add(new_aircraft)
    await db.commit()
    db_aircraft = await db.aircrafts.get_one(id=created_aircraft_db.id)

    assert db_aircraft is not None
    assert db_aircraft.name == new_aircraft.name
    assert db_aircraft.manufacturer == new_aircraft.manufacturer
    assert db_aircraft.id is not None

async def test_delete_aircraft(db, created_aircraft):
    await db.aircrafts.delete(id=created_aircraft.id)
    await db.commit()

    db_aircraft = await db.aircrafts.get_one_or_none(id=created_aircraft.id)
    assert db_aircraft is None

async def test_get_aircraft_by_id(db, created_aircraft):
    aircraft_db = await db.aircrafts.get_one_or_none(id=created_aircraft.id)
    assert aircraft_db
    assert aircraft_db.name == created_aircraft.name
    assert aircraft_db.manufacturer == created_aircraft.manufacturer

async def test_update_aircraft(db, created_aircraft):
    new_updated_data = {
        "name": "A330-800",
        "manufacturer": "A330 Family",
    }
    updated_aircraft = await db.aircrafts.edit(
        data=new_updated_data,
        id=created_aircraft.id,
    )
    await db.commit()
    updated_aircraft_db = await db.aircrafts.get_one(id=updated_aircraft.id)
    assert updated_aircraft_db is not None
    assert updated_aircraft_db.name == new_updated_data["name"]
    assert updated_aircraft_db.manufacturer == new_updated_data["manufacturer"]