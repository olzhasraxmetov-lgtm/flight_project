from app.repositories.users import UsersRepository
from app.repositories.airlines import AirlinesRepository
from app.repositories.airports import AirportsRepository
from app.repositories.flights import FlightsRepository
from app.repositories.aircrafts import AircraftsRepository
from app.repositories.seat_templates import SeatTemplatesRepository
from app.repositories.seat_template_seat import SeatTemplateSeatsRepository
from app.repositories.flight_instances import FlightInstancesRepository
from app.repositories.seat_instances_map import SeatInstancesMapRepository

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.airlines = AirlinesRepository(self.session)
        self.airports = AirportsRepository(self.session)
        self.flights = FlightsRepository(self.session)
        self.aircrafts = AircraftsRepository(self.session)
        self.seat_templates = SeatTemplatesRepository(self.session)
        self.seat_template_seats = SeatTemplateSeatsRepository(self.session)
        self.flight_instances = FlightInstancesRepository(self.session)
        self.seat_instances_map = SeatInstancesMapRepository(self.session)


        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()