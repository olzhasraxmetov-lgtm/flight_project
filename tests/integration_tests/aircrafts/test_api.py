import pytest

@pytest.mark.parametrize(
    "name, manufacturer, status_code", [
        ("A330-200", "Airbus A330", 200),
        ("A330-900", "Airbus A330 Family", 200),
        ("asd", "Airbus A330 Family", 422),
        ("A330-900", "aaa", 422),
    ]
)
async def test_create_aircraft(name, manufacturer, status_code, admin_user):
    response_create = await admin_user.post('/aircrafts', json={
        "name": name,
        "manufacturer": manufacturer,
    })

    assert response_create.status_code == status_code


async def test_get_all_aircraft_anonymous_forbidden(ac):
    """Проверяем, что даже без логина список недоступен"""
    response = await ac.get('/aircrafts')
    assert response.status_code == 401

async def test_admin_can_fully_update_aircraft(admin_user, created_aircraft):
    new_data = {
        "manufacturer": "Boeing 737-7",
        "name": "Boeing 737 MAX family",
    }

    response_create = await admin_user.put(f'/aircrafts/{created_aircraft.id}', json=new_data)
    data = response_create.json()

    assert response_create.status_code == 200
    assert data['name'] == new_data['name']
    assert data['manufacturer'] == new_data['manufacturer']
    assert 'id' in data

async def test_admin_can_partially_update_aircraft(admin_user, created_aircraft):
    new_data = {
        "name": "A330-200",
    }

    response_create = await admin_user.patch(f'/aircrafts/{created_aircraft.id}', json=new_data)
    data = response_create.json()

    assert response_create.status_code == 200
    assert data['name'] == new_data['name']
    assert data['manufacturer'] == created_aircraft.manufacturer

async def test_admin_can_delete_airport(admin_user, created_aircraft):

    response_create = await admin_user.delete(f'/aircrafts/{created_aircraft.id}')
    assert response_create.status_code == 204

    response_get = await admin_user.get(f'/aircrafts/{created_aircraft.id}')
    assert response_get.status_code == 404

async def test_aircraft_create_forbidden(auth_user):
    response = await auth_user.post('/aircrafts', json={})
    assert response.status_code == 403

async def test_aircraft_update_not_found(admin_user):
    response_create = await admin_user.put('/aircrafts/44', json={})
    assert response_create.status_code == 404
    assert response_create.json()["detail"] == "Самолет не найден"

async def test_aircraft_get_not_found(admin_user):
    response_get = await admin_user.get('/aircrafts/999')
    assert response_get.status_code == 404