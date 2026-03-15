from pydantic import BaseModel, Field, field_validator
from app.utils.check_valid_timezone import check_timezone

class AirportBase(BaseModel):
    code: str = Field(pattern=r"^[A-Z]{3}$", description="IATA код (напр. ALA)")
    name: str = Field(min_length=5, max_length=50, description="Название аэропорта")
    city: str = Field(min_length=3, max_length=30, description="Город")
    country: str = Field(min_length=2, max_length=30, description="Страна")
    timezone: str = Field(min_length=5, max_length=50, description="Часовой пояс")


    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        return check_timezone(value)


class AirportCreate(AirportBase):
    pass

class AirportUpdate(BaseModel):
    code: str | None = Field(None, pattern=r"^[A-Z]{3}$", min_length=3, max_length=3, description="IATA код аэропорта")
    name: str | None = Field(None, min_length=5, max_length=50, description="Название аэропорта")
    city: str | None = Field(None, min_length=3, max_length=30, description="Город в котором находится аэропорт")
    country: str | None = Field(None, min_length=2, max_length=30, description="Страна в котором находится аэропорт")
    timezone: str | None = Field(None, min_length=5, max_length=50, description="Часовой пояс")

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return check_timezone(value)

class AirportResponse(AirportBase):
    id: int

class AirportShort(BaseModel):
    id: int
    name: str
    code: str
    city: str