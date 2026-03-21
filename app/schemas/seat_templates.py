from pydantic import BaseModel, Field


class SeatTemplateBase(BaseModel):
    aircraft_model_id: int = Field(..., description="ID самолета")
    name: str = Field(...,min_length=6, max_length=50, description="Название шаблона")

class SeatTemplateResponse(SeatTemplateBase):
    id: int
    is_active: bool

class SeatTemplateCreate(SeatTemplateBase):
    pass
