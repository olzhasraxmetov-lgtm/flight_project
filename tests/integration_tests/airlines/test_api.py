import pytest


@pytest.mark.parametrize("iata_code, name, status_code",
    [
        ("CA", "Air China", 200),
        ("MU", "China Airlines", 200),
        ("a", "Air China", 422),
        ("a", "long name of airline", 422)
    ]
)
async def test_airlines_create(iata_code, name, status_code, admin_user):
    response_create = await admin_user.post('/airlines/', json={
        "iata_code": iata_code,
        "name": name,
    })
    assert response_create.status_code == status_code

@pytest.mark.parametrize("params, expected_len, expected_iata", [
    ({"page": 1, "per_page": 10}, 3, "IQ"),
    ({"name": "Air", "page": 1, "per_page": 2}, 2, "IQ"),
    ({"name": "NonExistent"}, 0, None),
])
async def test_get_all_airline(auth_user, db, params, expected_len, expected_iata):
    airlines = [
        {"iata_code": "IQ", "name": "Qazaq Air"},
        {"iata_code": "AA", "name": "American Airlines"},
        {"iata_code": "BA", "name": "British Airways"},
    ]
    await db.airlines.add_bulk(airlines)
    await db.commit()

    response = await auth_user.get('/airlines/', params=params)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == expected_len
    if expected_iata:
        assert any(item['iata_code'] == expected_iata for item in data)

@pytest.mark.parametrize(
    "page, per_page", [
    (0, 10),
    (-1, 10),
    (1, 0),
    (1, 101)
    ]
)
async def test_get_airlines_invalid_pagination(ac, page, per_page):
    response = await ac.get('/airlines/', params={"page": page, "per_page": per_page})

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'][-1] in ['page', 'per_page']


async def test_get_all_airlines_anonymous(ac, created_airline):
    """Проверяем, что даже без логина список доступен"""
    response = await ac.get('/airlines/')
    assert response.status_code == 200

async def test_airlines_update(admin_user, created_airline):
    new_data = {"iata_code": "NEW", "name": "Updated Name"}

    response_create = await admin_user.put(f'/airlines/{created_airline.id}', json=new_data)
    data = response_create.json()
    assert response_create.status_code == 200
    assert data['iata_code'] == new_data['iata_code']
    assert data['name'] == new_data['name']

async def test_airlines_partially_update(admin_user, created_airline):
    new_data = {"name": "Updated Name"}

    response_create = await admin_user.patch(f'/airlines/{created_airline.id}', json=new_data)
    data = response_create.json()
    assert response_create.status_code == 200
    assert data['name'] == new_data['name']
    assert data['iata_code'] == created_airline.iata_code

async def test_airlines_delete(admin_user, created_airline):

    response_create = await admin_user.delete(f'/airlines/{created_airline.id}')
    assert response_create.status_code == 204

    response_get = await admin_user.get(f'/airlines/{created_airline.id}')
    assert response_get.status_code == 404


async def test_airlines_create_forbidden(auth_user):
    response_create = await auth_user.post('/airlines/', json={
        "iata_code": 'JW',
        "name": 'Japan Airline',
    })
    assert response_create.status_code == 403

async def test_airlines_update_not_found(admin_user):
    response_create = await admin_user.put('/airlines/44', json={
        "iata_code": 'JW',
        "name": 'Japan Airline',
    })
    assert response_create.status_code == 404
    assert response_create.json()["detail"] == "Авиакомпания не найдена"


async def test_airline_get_not_found(auth_user):
    response_create = await auth_user.get('/airlines/999')
    assert response_create.status_code == 404