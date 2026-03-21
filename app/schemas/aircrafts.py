from pydantic import BaseModel, Field


class AircraftBase(BaseModel):
    name: str = Field(...,min_length=6, max_length=50, description="Название самолета")
    manufacturer: str = Field(min_length=6, max_length=30, description="Тип самолета")

class AircraftResponse(AircraftBase):
    id: int

class AircraftCreate(AircraftBase):
    pass
