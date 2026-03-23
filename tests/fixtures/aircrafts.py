from app.schemas.aircrafts import AircraftCreate
import pytest

@pytest.fixture
async def created_aircraft(db):
    """Фикстура, которая создает самолет для других тестов"""
    data = AircraftCreate(
        name='A330-900',
        manufacturer='Airbus neo Family',
    )
    aircraft = await db.aircrafts.add(data)
    await db.commit()
    return aircraft