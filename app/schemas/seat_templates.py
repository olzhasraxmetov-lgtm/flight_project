from pydantic import BaseModel, Field


class SeatTemplateBase(BaseModel):
    aircraft_model_id: int = Field(..., description="ID самолета")
    name: str = Field(...,min_length=6, max_length=50, description="Название шаблона")
    is_active: bool = Field(default=True, description="Активен ли шаблон")

class SeatTemplateResponse(SeatTemplateBase):
    id: int

class SeatTemplateCreate(SeatTemplateBase):
    pass
