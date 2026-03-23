from app.schemas.seat_templates import SeatTemplateCreate


async def test_create_seat_template(db, created_aircraft):
    new_seat_template = SeatTemplateCreate(
        aircraft_model_id=created_aircraft.id,
        name="A320 162 seats standard"
    )
    new_seat_template_db = await db.seat_templates.add(new_seat_template)
    await db.commit()
    db_seat_template = await db.seat_templates.get_one(id=new_seat_template_db.id)

    assert db_seat_template is not None
    assert db_seat_template.aircraft_model_id == new_seat_template.aircraft_model_id
    assert db_seat_template.name == new_seat_template.name
    assert db_seat_template.id is not None

async def test_get_all_seat_templates(db, several_templates):
    templates = await db.seat_templates.get_all()
    assert len(templates) == len(several_templates)

async def test_delete_seat_template(db, created_seat_template):
    await db.seat_templates.delete(id=created_seat_template.id)
    await db.commit()

    db_seat_template = await db.seat_templates.get_one_or_none(id=created_seat_template.id)
    assert db_seat_template is None

async def test_get_seat_template_by_id(db, created_seat_template):
    seat_template_db = await db.seat_templates.get_one_or_none(id=created_seat_template.id)
    assert seat_template_db
    assert seat_template_db.name == created_seat_template.name
    assert seat_template_db.aircraft_model_id == created_seat_template.aircraft_model_id

async def test_update_seat_template(db, created_seat_template):
    new_updated_data = {
        "aircraft_model_id": 1,
        "name": "Standard Regional (192 seats)",
    }
    updated_seat_template = await db.seat_templates.edit(
        data=new_updated_data,
        id=created_seat_template.id,
    )
    await db.commit()
    updated_seat_template_db = await db.seat_templates.get_one(id=updated_seat_template.id)
    assert updated_seat_template_db is not None
    assert updated_seat_template_db.name == new_updated_data["name"]