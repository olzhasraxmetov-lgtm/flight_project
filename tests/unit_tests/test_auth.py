from app.services.users import UsersService


def test_create_access_token(db):
    data = {"user_id": 1}
    jwt_token = UsersService(db).create_access_token(data=data) # type: ignore

    assert jwt_token
    assert isinstance(jwt_token, str)