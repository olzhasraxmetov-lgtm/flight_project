from .users import UsersORM
from .airlines import AirlinesORM
from .airports import AirportsORM
from .flights import FlightsORM
from .aircrafts import AircraftsORM
from .seat_templates import SeamTemplatesORM
from .seat_template_seat import SeatTemplateSeatsORM


__all__ = ["UsersORM", "AirlinesORM", "AirportsORM", "FlightsORM", "AircraftsORM", "SeamTemplatesORM", "SeatTemplateSeatsORM"]