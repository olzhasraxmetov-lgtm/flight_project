from app.schemas.seat_template_seats import SeatTemplateSeatCreate, SeatTemplateSeatBase
from app.services.base import BaseService
from app.helpers.seat_type import SeatType
from app.helpers.cabin_class import CabinClass

class SeatTemplateSeatsService(BaseService):
    async def seat_template_seat_create(self, payload: SeatTemplateSeatCreate):
        LETTERS = ["A", "B", "C", "D", "E", "F"]
        seats_to_create = []
        for row in range(1, payload.rows_count + 1):
            current_class = CabinClass.BUSINESS if row <= payload.business_class_rows else CabinClass.ECONOMY

            for letter in LETTERS:
                if current_class == CabinClass.BUSINESS and letter in ["B", "E"]:
                    continue

                if letter in ["A", "F"]:
                    stype = SeatType.WINDOW
                elif letter in ["C", "D"]:
                    stype = SeatType.AISLE
                else:
                    stype = SeatType.MIDDLE
                seats_to_create.append({
                    "seat_template_id": payload.seat_template_id,
                    "seat_number": f"{row}{letter}",
                    "seat_type": stype,
                    "cabin_class": current_class
                })
        await self.db.seat_template_seats.add_bulk(seats_to_create)
        await self.db.commit()