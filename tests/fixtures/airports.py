from app.schemas.airports import AirportCreate
import pytest

@pytest.fixture
async def created_airport(db):
    """Фикстура, которая создает аэропорт для других тестов"""
    data = AirportCreate(
        code='SCO',
        name='Almaty International',
        city='Almaty',
        country='Kazakhstan',
        timezone='Asia/Almaty'
    )
    airport = await db.airports.add(data)
    await db.commit()
    return airport