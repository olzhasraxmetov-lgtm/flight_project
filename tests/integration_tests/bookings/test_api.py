async def test_create_booking_api(db, auth_user, created_flight_instance):
    all_seats = await db.seat_instances_map.get_all(flight_instance_id=created_flight_instance.id)

    payload = {
        "flight_instance_id": created_flight_instance.id,
        "passengers": [
            {
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "passport_number": "AB12345",
                "seat_instance_id": all_seats[0].id
            }
        ]
    }

    response = await auth_user.post("/bookings", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "booking_reference" in data
    assert len(data["passengers"]) == 1

async def test_get_my_bookings_api(db, auth_user, created_booking):
    response = await auth_user.get("/bookings/my")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id"] == created_booking.id
    assert data[0]["passengers_count"] == len(created_booking.passengers)

async def test_get_my_booking_by_id_api(db, auth_user, created_booking):
    response = await auth_user.get(f"/bookings/{created_booking.id}")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "booking_reference" in data
    assert data["status"] == "created"

async def test_not_found_booking_by_id_api(db, auth_user, created_booking):
    response = await auth_user.get("/bookings/34")

    assert response.status_code == 404
    assert response.json()["detail"] == "Бронирование не найдено"

async def test_delete_booking_api(db, auth_user, created_booking):
    response = await auth_user.delete(f"/bookings/{created_booking.id}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Бронирование успешно удалено"

    response = await auth_user.get(f"/bookings/{created_booking.id}")
    assert response.status_code == 404

async def test_delete_passenger_in_booking_api(db, auth_user, created_booking):
    passenger_id = created_booking.passengers[0].id
    total_price = created_booking.total_price
    response = await auth_user.delete(f"/bookings/{created_booking.id}/passenger/{passenger_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == f"Passenger {passenger_id} removed"
    assert data["new_total_price"] != total_price

async def test_delete_passenger_not_found_in_booking_api(db, auth_user, created_booking):
    response = await auth_user.delete(f"/bookings/{created_booking.id}/passenger/1111111")
    assert response.status_code == 404
    assert response.json()["detail"] == "Пассажир не найден"

async def test_get_my_bookings_unauthorized(ac):
    response = await ac.get("/bookings/my")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

async def test_create_booking_invalid_payload(auth_user):
    payload = {"flight_instance_id": "invalid", "passengers": []}
    response = await auth_user.post("/bookings", json=payload)
    assert response.status_code == 422