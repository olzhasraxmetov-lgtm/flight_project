from pydantic import BaseModel, Field

class AirportBase(BaseModel):
    code: str = Field(pattern=r"^[A-Z]{3}$", description="IATA код (напр. ALA)")
    name: str = Field(min_length=5, max_length=50, description="Название аэропорта")
    city: str = Field(min_length=3, max_length=30, description="Город")
    country: str = Field(min_length=2, max_length=30, description="Страна")
    timezone: str = Field(min_length=5, max_length=50, description="Часовой пояс")


class AirportCreate(AirportBase):
    pass

class AirportUpdate(BaseModel):
    code: str | None = Field(None, min_length=3, max_length=3, description="IATA код аэропорта")
    name: str | None = Field(None, min_length=10, max_length=50, description="Название аэропорта")
    city: str | None = Field(None, min_length=10, max_length=20, description="Город в котором находится аэропорт")
    country: str | None = Field(None, min_length=10, max_length=20, description="Страна в котором находится аэропорт")
    timezone: str | None = Field(None, min_length=10, max_length=50, description="Часовой пояс")

class AirportResponse(AirportBase):
    id: int

