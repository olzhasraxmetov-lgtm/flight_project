import pytest

@pytest.mark.parametrize(
    "name, status_code", [
        ("Standard Regional (162 seats)", 200),
        ("asd", 422),
    ]
)
async def test_create_new_seat_template(name, created_aircraft, status_code, admin_user):
    response_create = await admin_user.post('/seat_templates', json={
        "name": name,
        "aircraft_model_id": created_aircraft.id,
    })

    assert response_create.status_code == status_code


async def test_get_all_seat_templates_anonymous_forbidden(ac):
    """Проверяем, что даже без логина список недоступен"""
    response = await ac.get('/seat_templates')
    assert response.status_code == 401

async def test_admin_can_fully_update_seat_template(admin_user, created_seat_template):
    new_data = {
        "aircraft_model_id": 1,
        "is_active": False,
        "name": "Standard Regional Business",
    }

    response_create = await admin_user.put(f'/seat_templates/{created_seat_template.id}', json=new_data)
    data = response_create.json()

    assert response_create.status_code == 200
    assert data['name'] == new_data['name']
    assert 'id' in data
#
async def test_admin_can_partially_update_seat_template(admin_user, created_seat_template):
    new_data = {
        "name": "Standard Regional Economy",
    }

    response_create = await admin_user.patch(f'/seat_templates/{created_seat_template.id}', json=new_data)
    data = response_create.json()

    assert response_create.status_code == 200
    assert data['name'] == new_data['name']
    assert data['is_active'] == created_seat_template.is_active

async def test_admin_can_delete_seat_template(admin_user, created_seat_template):

    response_create = await admin_user.delete(f'/seat_templates/{created_seat_template.id}')
    assert response_create.status_code == 204

    response_get = await admin_user.get(f'/seat_templates/{created_seat_template.id}')
    assert response_get.status_code == 404

async def test_seat_template_create_forbidden(auth_user):
    response = await auth_user.post('/seat_templates', json={})
    assert response.status_code == 403

async def test_seat_template_update_not_found(admin_user):
    response_create = await admin_user.put('/seat_templates/44', json={})
    assert response_create.status_code == 404
    assert response_create.json()["detail"] == "Шаблон самолета не найден"

async def test_seat_template_get_not_found(admin_user):
    response_get = await admin_user.get('/seat_templates/999')
    assert response_get.status_code == 404