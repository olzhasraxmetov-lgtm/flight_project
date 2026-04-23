from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.database import AsyncSessionLocal
from app.helpers.users_role import UserRoleEnum
from app.repositories.users import UsersRepository
from app.services.users import UsersService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        async with AsyncSessionLocal() as session:
            repo = UsersRepository(session)
            user = await repo.get_one_or_none(email=email, map_res=False)

            if not user or not UsersService().verify_password(password, user.hashed_password):
                return False

            if user.role != UserRoleEnum.ADMIN:
                return False

            request.session.update({"user_id": str(user.id)})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")

        if not user_id:
            return False

        return True

