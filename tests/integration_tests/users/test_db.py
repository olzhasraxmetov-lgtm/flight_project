from app.schemas.users import UserCreate
from app.services.users import UsersService

async def test_create_user(db):
    user_data = UserCreate(
        email="olzhas@gmail.com", # type: ignore
        hashed_password=UsersService.password_hash.hash("olzhas123"),
        username="olzhas",
        phone="+7-775-295-5102", # type: ignore

    )
    await db.users.add(user_data)
    await db.commit()

    new_user = await db.users.get_one_or_none(email="olzhas@gmail.com")
    assert new_user
    assert new_user.email == "olzhas@gmail.com"
