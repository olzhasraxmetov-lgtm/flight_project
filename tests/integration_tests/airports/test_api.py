import pytest

@pytest.mark.parametrize(
    "code, name, city, country, timezone, status_code", [
        ("ALA", "Almaty International", "Almaty", "Kazakhstan", "Asia/Almaty", 200),
        ("NQZ", "Nursultan Nazarbayev", "Astana", "Kazakhstan", "Asia/Almaty", 200),
        ("asd", "wrong_iata_code", "Almaty", "Kazakhstan", "Asia/Almaty", 422),
        ("ALA", "Almaty International", "sd", "Kazakhstan", "Asia/Almaty", 422),
        ("ALA", "wrong_timezone", "Almaty", "Kazakhstan", "Asia/", 422)
    ]
)
async def test_create_airport(code, name, city, country, timezone, status_code, admin_user):
    response_create = await admin_user.post('/airports', json={
        "code": code,
        "name": name,
        "city": city,
        "country": country,
        "timezone": timezone,
    })

    assert response_create.status_code == status_code


@pytest.mark.parametrize(
    "params, expected_len, expected_code", [
        ({"country": "key", "page": 1, "per_page": 10}, 2, "IST"),
        ({"country": "stan", "page": 1, "per_page": 10}, 2, "SCO"),
        ({"country": "stan", "name": "international", "page": 1, "per_page": 10}, 2, "NQZ"),
        ({}, 4, "IST"),
        ({"name": "NonExistName"}, 0, None),
    ]
)
async def test_get_airports_with_pagination(
        ac, db, params, expected_len, expected_code, init_cache
):
    airports = [
        {
            "code": "IST",
            "name": "Istanbul Airport",
            "city": "Istanbul",
            "country": "Turkey",
            "timezone": "Europe/Istanbul"
        },
        {
            "code": "AYT",
            "name": "Antalya International Airport",
            "city": "Antalya",
            "country": "Turkey",
            "timezone": "Europe/Istanbul"
        },
        {
            "code": "SCO",
            "name": "Aktau International Airport",
            "city": "Aktau",
            "country": "Kazakhstan",
            "timezone": "Asia/Aqtau"
        },
        {
            "code": "NQZ",
            "name": "Nursultan Nazarbayev International Airport",
            "city": "Astana",
            "country": "Kazakhstan",
            "timezone": "Asia/Almaty"
        }
    ]

    await db.airports.add_bulk(airports)
    await db.commit()

    response = await ac.get('/airports', params=params)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == expected_len

    if expected_code:
        assert any(item['code'] == expected_code for item in data)


@pytest.mark.parametrize(
    "page, per_page", [
    (0, 10),
    (-1, 10),
    (1, 0),
    (1, 101)
    ]
)
async def test_get_airports_invalid_pagination(ac, page, per_page):
    response = await ac.get('/airports', params={"page": page, "per_page": per_page})

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'][-1] in ['page', 'per_page']

async def test_get_all_airports_anonymous(ac):
    """Проверяем, что даже без логина список доступен"""
    response = await ac.get('/airports')
    assert response.status_code == 200

async def test_admin_can_fully_update_airport(admin_user, created_airport):
    new_data = {
        "code": "NQZ",
        "name": "Nursultan Nazarbayev",
        "city": "Astana",
        "country": "Kazakhstan",
        "timezone": "Asia/Almaty"
    }

    response_create = await admin_user.put(f'/airports/{created_airport.id}', json=new_data)
    data = response_create.json()

    assert response_create.status_code == 200
    assert data['code'] == new_data['code']
    assert data['name'] == new_data['name']
    assert data['city'] == new_data['city']
    assert 'id' in data

async def test_admin_can_partially_update_airport(admin_user, created_airport):
    new_data = {
        "code": "NQZ",
        "name": "Nursultan Nazarbayev",
        "city": "Astana"
    }

    response_create = await admin_user.patch(f'/airports/{created_airport.id}', json=new_data)
    data = response_create.json()

    assert response_create.status_code == 200
    assert data['code'] == new_data['code']
    assert data['name'] == new_data['name']
    assert data['city'] == new_data['city']
    assert data['country'] == created_airport.country
    assert data['timezone'] == created_airport.timezone

async def test_admin_can_delete_airport(admin_user, created_airport):

    response_create = await admin_user.delete(f'/airports/{created_airport.id}')
    assert response_create.status_code == 204

    response_get = await admin_user.get(f'/airports/{created_airport.id}')
    assert response_get.status_code == 404

async def test_airport_create_forbidden(auth_user):
    response = await auth_user.post('/airports', json={
        "code": "NQZ",
        "name": "Nursultan Nazarbayev",
        "city": "Astana",
        "country": "Kazakhstan",
        "timezone": "Asia/Almaty"
    })
    assert response.status_code == 403

async def test_airport_update_not_found(admin_user):
    response_create = await admin_user.put('/airports/44', json={
        "code": "NQZ",
        "name": "Nursultan Nazarbayev",
        "city": "Astana",
        "country": "Kazakhstan",
        "timezone": "Asia/Almaty"
    })
    assert response_create.status_code == 404
    assert response_create.json()["detail"] == "Аэропорт не найден"

async def test_airport_get_not_found(auth_user):
    response_get = await auth_user.get('/airports/999')
    assert response_get.status_code == 404