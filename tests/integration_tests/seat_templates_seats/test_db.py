from app.services.seat_template_seats import SeatTemplateSeatsService

async def test_create_seat_template_seats(db, admin_user, created_seat_template):
    service = SeatTemplateSeatsService(db)

    data = service.generate_seat_template(
        seat_template_id=created_seat_template.id,
        rows=12,
        business_class_rows=3,
    )
    await db.seat_template_seats.add_bulk(data)
    await db.commit()

    seats = await db.seat_template_seats.get_ordered_and_filters_seats(template_id=created_seat_template.id)
    assert len(seats) == 66

async def test_get_seat_template_seats_by_id(db, admin_user, created_seat_templates_seats, created_seat_template):
    seats = await db.seat_template_seats.get_ordered_and_filters_seats(template_id=created_seat_template.id)
    assert isinstance(seats, list)
    assert len(seats) == 162
    assert seats[0].seat_number.strip() == "1A"

async def test_delete_seat_template_seats_by_id(db, admin_user, created_seat_template):
    await db.seat_template_seats.delete_by_template_id(created_seat_template.id)
    await db.commit()
    remaining_seats = await db.seat_template_seats.get_ordered_and_filters_seats(
        template_id=created_seat_template.id
    )

    assert len(remaining_seats) == 0
    assert isinstance(remaining_seats, list)