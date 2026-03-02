from sqlalchemy import select

from app.mappers.users import UserMapper
from app.mappers.users import UserMapperWithPassword
from app.models.users import UsersORM
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserMapper

    async def get_user_with_hashed_password(self, email: str):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return UserMapperWithPassword.map_to_domain_entity(model)