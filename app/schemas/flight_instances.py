from pydantic import BaseModel


class FlightInstanceResponse(BaseModel):
    id: int