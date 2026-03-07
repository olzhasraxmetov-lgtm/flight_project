from app.mappers.base import DataMapper
from app.models.airlines import AirlinesORM
from app.schemas.airlines import AirlineResponse

class AirlinesMapper(DataMapper):
    db_model: AirlinesORM
    schema: AirlineResponse