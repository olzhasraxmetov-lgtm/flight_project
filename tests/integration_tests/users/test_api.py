import pytest


@pytest.mark.parametrize(
    "email,password, username, phone, status_code",
    [
        ("olzhas@gmail.com", "somepass123", "user_56", "+77022955423", 200),
        ("new_user@gmail.com", "easypassword", "abc", "invalid_phone", 422),
        ("user_user@gmail.com", "gggssq654", "user_12", "+77752953343", 200),
    ]
)
async def test_user_flow(
        email: str, password: str,
        username: str, phone: str,
        status_code: int,
        ac
):
    response_register = await ac.post(
        "/users/register",
        json={
            "email": email,
            "phone": phone,
            "username": username,
            "password": password,
        }
    )
    assert response_register.status_code == status_code
    if status_code != 200:
        return

    response_login = await ac.post(
        "/users/login",
        json={
            "email": email,
            "password": password,
        }
    )
    response_login_data = response_login.json()
    assert response_login.status_code == status_code
    assert 'access_token' in response_login_data

    response_get_profile = await ac.get("/users/me")
    get_profile_data = response_get_profile.json()
    assert response_get_profile.status_code == status_code
    assert isinstance(get_profile_data, dict)
    assert 'email' in get_profile_data
    assert 'id' in get_profile_data
    assert "password" not in get_profile_data
    assert "hashed_password" not in get_profile_data

    response_logout = await ac.post('/users/logout')
    logout_data = response_logout.json()
    assert response_logout.status_code == status_code
    assert logout_data["status"] == "success"
    assert not ac.cookies.get("access_token")

async def test_user_registration_duplicate(ac):
    user_data = {
        "email": "copy@me.com",
        "password": "copycopy123",
        "username": "user_copy",
        "phone": "+77752955102"
    }

    await ac.post("/users/register", json=user_data)

    response = await ac.post("/users/register", json=user_data)

    assert response.status_code == 409
    assert response.json()["detail"] == "Пользователь с такой почтой уже существует"