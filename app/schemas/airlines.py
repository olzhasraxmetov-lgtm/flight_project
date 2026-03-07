from pydantic import BaseModel, Field

class AirlineBase(BaseModel):
    iata_code: str = Field(min_length=2, max_length=3, description="IATA код (напр. KC)")
    name: str = Field(min_length=4, max_length=20, description='Название авиакомпаний')

class AirlineCreate(AirlineBase):
    pass

class AirlineUpdate(BaseModel):
    iata_code: str | None = None
    name: str | None = None

class AirlineResponse(AirlineBase):
    id: int