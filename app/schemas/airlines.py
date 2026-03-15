from pydantic import BaseModel, Field

class AirlineBase(BaseModel):
    iata_code: str = Field(min_length=2, max_length=3, description="IATA код (напр. KC)")
    name: str = Field(min_length=4, max_length=20, description='Название авиакомпаний')

class AirlineCreate(AirlineBase):
    pass

class AirlineUpdate(BaseModel):
    iata_code: str | None = Field(None, min_length=2, max_length=3)
    name: str | None = Field(None, min_length=4, max_length=20)

class AirlineResponse(AirlineBase):
    id: int

class AirlineShort(BaseModel):
    id: int
    name: str