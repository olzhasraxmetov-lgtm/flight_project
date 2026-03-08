import pytest


@pytest.fixture(scope="function")
async def registered_user(db):
    user_data = {
        "email": "auth_user@gmail.com",
        "hashed_password": "12345",
        "username": "auth_user",
        "phone": "+7-775-295-5102",
        "role": "user"
    }
    user = await db.users.add(user_data)
    await db.commit()
    return user

@pytest.fixture(scope="function")
async def registered_admin(db):
    user_data = {
        "email": "admin@gmail.com",
        "hashed_password": "12345",
        "username": "admin_super123",
        "phone": "+7-775-295-6102",
        "role": "admin"
    }
    user = await db.users.add(user_data)
    await db.commit()
    return user