from app.services.users import UsersService


def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = UsersService().create_access_token(data=data)

    assert jwt_token
    assert isinstance(jwt_token, str)