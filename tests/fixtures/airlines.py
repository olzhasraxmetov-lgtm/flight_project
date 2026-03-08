from app.schemas.airlines import AirlineCreate
import pytest

@pytest.fixture
async def created_airline(db):
    """Фикстура, которая создает авиакомпанию для других тестов"""
    data = AirlineCreate(iata_code='JT', name='Avia Jaynar')
    airline = await db.airlines.add(data)
    await db.commit()
    return airline