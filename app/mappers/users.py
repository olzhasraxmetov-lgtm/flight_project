from app.mappers.base import DataMapper
from app.models.users import UsersORM
from app.schemas.users import UserResponse, UserWithHashedPassword


class UserMapper(DataMapper):
    db_model = UsersORM
    schema = UserResponse

class UserMapperWithPassword(UserMapper):
    schema = UserWithHashedPassword