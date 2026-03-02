from app.models.users import UsersORM
from app.repositories.base import BaseRepository
from app.mappers.users import UserMapper

class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserMapper