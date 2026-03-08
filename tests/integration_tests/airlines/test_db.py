from app.schemas.airlines import AirlineCreate

async def test_get_airline_by_id(db, created_airline):
    airline_db = await db.airlines.get_one_or_none(id=created_airline.id)
    assert airline_db
    assert airline_db.iata_code == created_airline.iata_code
    assert airline_db.name == created_airline.name

async def test_list_of_airline(db):
    first_data = AirlineCreate(
        iata_code='JT',
        name='Avia Jaynar'
    )
    second_data = AirlineCreate(
        iata_code='DV',
        name='Scat'
    )

    await db.airlines.add_bulk([first_data, second_data])
    await db.commit()

    db_airlines = await db.airlines.get_all()
    assert len(db_airlines) == 2

async def test_add_airline(db):
    new_airline_data = AirlineCreate(
        iata_code='JT',
        name='Avia Jaynar'
    )
    new_airline = await db.airlines.add(new_airline_data)

    new_airline_db = await db.airlines.get_one_or_none(id=new_airline.id)

    assert new_airline_db
    assert new_airline_db.iata_code == new_airline.iata_code
    assert new_airline_db.name == new_airline.name

    await db.commit()

async def test_delete_airline(db, created_airline):
    await db.airlines.delete(id=created_airline.id)
    await db.commit()

    db_airline = await db.airlines.get_one_or_none(id=created_airline.id)
    assert db_airline is None

async def test_update_airline(db, created_airline):
    new_name = "New Avia Name"
    await db.airlines.edit(
        data={"name": new_name},
        id=created_airline.id,
    )
    await db.commit()

    db_airline = await db.airlines.get_one_or_none(id=created_airline.id)
    assert db_airline.name == new_name

