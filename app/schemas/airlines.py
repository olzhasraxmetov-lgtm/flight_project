from pydantic import BaseModel, Field

class AirlineBase(BaseModel):
    code: str = Field(min_length=3, max_length=3, description="IATA код (напр. KC)")
    name: str = Field(min_length=6, max_length=20, description='Название авиакомпаний')

class AirlineCreate(AirlineBase):
    pass

class AirlineUpdate(BaseModel):
    code: str | None = None
    name: str | None = None

class AirlineResponse(AirlineBase):
    id: int