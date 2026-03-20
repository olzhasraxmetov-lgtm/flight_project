from decimal import Decimal

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
async def test_get_flights_pagination_params(ac, params, expected_status):
    response = await ac.get("/flights", params=params)
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    "custom_data, expected_status", [

        ({"flight_number": "TOO_LONG_NAME_12345"}, 422),

        ({"price": -100}, 422),

        ({
             "departure_at": "2026-03-25T15:00:00Z",
             "arrival_at": "2026-03-25T10:00:00Z"
         }, 400),
    ]
)
async def test_create_flight(admin_user, seed_data, custom_data, expected_status):
    payload = {
        "flight_number": "KC-851",
        "departure_at": "2026-03-25T10:00:00Z",
        "arrival_at": "2026-03-25T12:00:00Z",
        "price": 25000,
        "departure_airport_id": seed_data["ala_id"],
        "arrival_airport_id": seed_data["nqz_id"],
        "airline_id": seed_data["airline_id"]
    }

    payload.update(custom_data)

    response = await admin_user.post('/flights', json=payload)

    assert response.status_code == expected_status


async def test_get_all_flights_anonymous(ac):
    """Проверяем, что даже без логина список доступен"""
    response = await ac.get('/flights')
    assert response.status_code == 200

async def test_admin_can_fully_update_flight(admin_user, flight_update_data):
    flight = flight_update_data["flight"]

    new_data = {
        "flight_number": "IQ-777",
        "price": 15000,
        "departure_airport_id": flight_update_data["new_airport_id"],
        "airline_id": flight_update_data["new_airline_id"],
        "arrival_airport_id": flight.arrival_airport_id,
        "departure_at": flight.departure_at.isoformat(),
        "arrival_at": flight.arrival_at.isoformat(),
    }

    response_create = await admin_user.put(f'/flights/{flight.id}', json=new_data)
    data = response_create.json()

    assert response_create.status_code == 200
    assert 'id' in data

async def test_admin_can_partially_update_airport(admin_user, flight_update_data):
    flight = flight_update_data["flight"]

    new_data = {
        "flight_number": "KCA-999",
        "price": 15000.00,
    }

    response_update = await admin_user.patch(f'/flights/{flight.id}', json=new_data)
    data = response_update.json()

    assert response_update.status_code == 200
    assert data['flight_number'] == new_data['flight_number']
    assert Decimal(data['price']) == new_data['price']
    assert data['departure_airport_id'] == flight.departure_airport_id
    assert data['arrival_airport_id'] == flight.arrival_airport_id

async def test_admin_can_delete_flight(admin_user, created_flight):

    response_delete = await admin_user.delete(f'/flights/{created_flight.id}')
    assert response_delete.status_code == 204

    response_get = await admin_user.get(f'/flights/{created_flight.id}')
    assert response_get.status_code == 404

async def test_flight_create_forbidden(auth_user):
    response = await auth_user.post('/flights', json={})
    assert response.status_code == 403

async def test_flight_update_not_found(admin_user):
    response_update = await admin_user.put('/flights/44', json={})
    assert response_update.status_code == 404
    assert response_update.json()["detail"] == "Рейс не найден"

async def test_flight_get_not_found(auth_user):
    response_get = await auth_user.get('/flights/999')
    assert response_get.status_code == 404