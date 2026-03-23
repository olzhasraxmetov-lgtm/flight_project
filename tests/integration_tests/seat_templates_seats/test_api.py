async def test_create_new_seat_template_seats(admin_user, created_seat_template):
    response_create = await admin_user.post('/seat_template_seats', json={
          "seat_template_id": created_seat_template.id,
          "rows_count": 28,
          "business_class_rows": 3,
          "first_class_rows": 0
    })
    data = response_create.json()

    assert response_create.status_code == 200
    assert data["message"] == "Seats generated successfully"
    assert data["template_id"] == created_seat_template.id
    assert data["count"] == 162

async def test_get__seat_template_seats(admin_user, created_seat_template, created_seat_templates_seats):
    response_create = await admin_user.get(f'/seat_template_seats/{created_seat_template.id}/seats')
    data = response_create.json()

    assert response_create.status_code == 200
    assert data["template_id"] == created_seat_template.id
    assert data["total_seats"] == 162
    assert "rows" in data
    assert data["rows"]["1"][0]["no"] == "1A"
    assert isinstance(data["rows"]["1"], list)
    first_seat = data["rows"]["1"][0]
    expected_keys = {"id", "no", "cabin_class", "seat_type"}
    assert set(first_seat.keys()) == expected_keys

async def test_get_seats_not_found(admin_user):
    response = await admin_user.get('/seat_template_seats/999999/seats')
    assert response.status_code == 404

async def test_delete_seats(admin_user, created_seat_template):
    response = await admin_user.delete(f'/seat_template_seats/{created_seat_template.id}')

    assert response.status_code == 204
    get_response = await admin_user.get(f'/seat_template_seats/{created_seat_template.id}/seats')
    data = get_response.json()
    assert data["total_seats"] == 0
    assert len(data["rows"]) == 0

async def test_create_seats_anonymous_forbidden(ac):
    response_create = await ac.post('/seat_template_seats', json={})
    assert response_create.status_code == 401

async def test_get_seats_anonymous_forbidden(ac):
    response = await ac.get('/seat_template_seats/1/seats')
    assert response.status_code == 401