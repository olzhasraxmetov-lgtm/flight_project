from app.models.passengers import PassengersORM
from app.repositories.base import BaseRepository

class PassengersRepository(BaseRepository):
    model = PassengersORM