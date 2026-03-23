from pydantic import BaseModel, Field
from app.helpers.cabin_class import CabinClass
from app.helpers.seat_type import SeatType

class SeatTemplateSeatBase(BaseModel):
    seat_template_id: int = Field(..., description="ID шаблона места")
    seat_number: str = Field(..., min_length=3, max_length=4, description="Номер места")
    cabin_class: CabinClass = Field(description="Класс места")
    seat_type: SeatType = Field(description="Тип места")
    row_number: int
    seat_letter: str

class SeatTemplateSeatResponse(SeatTemplateSeatBase):
    id: int

class SeatTemplateSeatCreate(BaseModel):
    seat_template_id: int = Field(..., description="ID шаблона места")
    rows_count: int = Field(..., description="Количество рядов")
    business_class_rows: int = Field(description="Количество рядов бизнес класса")
    first_class_rows: int = Field(description="Количество рядов первого класса")

class SeatGenerationResponse(BaseModel):
    message: str = "Seats generated successfully"
    template_id: int
    count: int

class SeatShortResponse(BaseModel):
    id: int
    no: str
    cabin_class: CabinClass
    seat_type: SeatType

class SeatTemplateMapResponse(BaseModel):
    template_id: int
    total_seats: int
    rows: dict[str, list[SeatShortResponse]]