import pytest

@pytest.mark.parametrize(
    "params, expected_status", [
        ({"page": 1, "per_page": 10}, 200),
        ({"page": 0, "per_page": 10}, 422),
        ({"page": -1, "per_page": 10}, 422),
        ({"page": 1, "per_page": 0}, 422),
        ({"page": 1, "per_page": 101}, 422),
    ]
)
async def test_get_flight_instances_pagination_params(ac, params, expected_status):
    response = await ac.get("/flight_instances", params=params)
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    "custom_data, expected_status", [

        ({"flight_number": "TOO_LONG_NAME_12345"}, 422),

        ({"price": -100}, 422),

        ({
             "departure_at": "2026-03-25T15:00:00Z",
             "arrival_at": "2026-03-25T10:00:00Z"
         }, 422 ),
    ]
)
async def test_create_flight_instance(admin_user, seed_data, custom_data, expected_status, created_seat_template):
    payload = {
        "flight_number": "KC-851",
        "departure_at": "2026-03-25T10:00:00Z",
        "arrival_at": "2026-03-25T12:00:00Z",
        "base_price": 25000,
        "seat_template_id": created_seat_template.id,
        "departure_airport_id": seed_data["ala_id"],
        "arrival_airport_id": seed_data["nqz_id"],
    }

    payload.update(custom_data)

    response = await admin_user.post('/flight_instances', json=payload)

    assert response.status_code == expected_status

async def test_get_all_flight_instances_anonymous(ac):
    """Проверяем, что даже без логина список доступен"""
    response = await ac.get('/flight_instances')
    assert response.status_code == 200

async def test_get_flight_instance_map_anonymous(ac, created_flight_instance):
    response = await ac.get(f"/flight_instances/{created_flight_instance.id}/seats")
    data = response.json()
    assert response.status_code == 200
    assert data["flight_instance_id"] == created_flight_instance.id
    assert data["total_seats"] > 0
    assert "rows" in data

async def test_admin_can_update_flight_instance_status(ac, admin_user, created_flight_instance):
    response = await admin_user.patch(f'/flight_instances/{created_flight_instance.id}/status', json={
        "status": "delayed"
    })
    data = response.json()
    assert data["status"] != created_flight_instance.status

async def test_flight_instances_create_forbidden(auth_user):
    response = await auth_user.post('/flight_instances', json={})
    assert response.status_code == 403

async def test_flight_instances_update_status_forbidden(auth_user, created_flight_instance):
    response = await auth_user.patch(f'/flight_instances/{created_flight_instance.id}/status', json={})
    assert response.status_code == 403