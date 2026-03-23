import pytest
from app.schemas.seat_templates import SeatTemplateCreate

@pytest.fixture
async def created_seat_template(db, created_aircraft):
    new_seat_template = SeatTemplateCreate(
        aircraft_model_id=created_aircraft.id,
        name="Standard Regional (162 seats"
    )
    new_seat_template_db = await db.seat_templates.add(new_seat_template)
    await db.commit()
    return new_seat_template_db

@pytest.fixture
async def several_templates(db, created_aircraft):
    """Создает 3 шаблона для тестов списка"""
    templates = []
    for i in range(3):
        data = SeatTemplateCreate(
            aircraft_model_id=created_aircraft.id,
            name=f"Test Layout {i}"
        )
        t = await db.seat_templates.add(data)
        templates.append(t)
    await db.commit()
    return templates