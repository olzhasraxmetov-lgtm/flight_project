import pytest
from app.services.seat_template_seats import SeatTemplateSeatsService

@pytest.fixture
async def created_seat_templates_seats(db, created_seat_template):
    service = SeatTemplateSeatsService(db)

    data = service.generate_seat_template(
        seat_template_id=created_seat_template.id,
        rows=28,
        business_class_rows=3,
    )
    await db.seat_template_seats.add_bulk(data)
    await db.commit()

    return data