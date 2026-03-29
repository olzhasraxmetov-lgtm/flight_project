import pytest
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.core.database import async_session_maker_null_poll, engine_null_pool, Base
from app.utils.db_manager import DBManager
from app.main import app
from app.core.dependencies import get_db, get_current_user

pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.airlines",
    "tests.fixtures.airports",
    "tests.fixtures.flights",
    "tests.fixtures.aircrafts",
    "tests.fixtures.seat_templates",
    "tests.fixtures.seat_templates_seats",
    "tests.fixtures.flight_instances",
]

@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        yield db

@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="function", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="function")
async def auth_user(registered_user, ac):
    app.dependency_overrides[get_current_user] = lambda: registered_user

    yield ac

    del app.dependency_overrides[get_current_user]

@pytest.fixture(scope="function")
async def admin_user(registered_admin, ac):
    app.dependency_overrides[get_current_user] = lambda: registered_admin

    yield ac

    del app.dependency_overrides[get_current_user]