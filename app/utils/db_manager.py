from app.repositories.users import UsersRepository
from app.repositories.airlines import AirlinesRepository
from app.repositories.airports import AirportsRepository
from app.repositories.flights import FlightsRepository

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.airlines = AirlinesRepository(self.session)
        self.airports = AirportsRepository(self.session)
        self.flights = FlightsRepository(self.session)


        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()