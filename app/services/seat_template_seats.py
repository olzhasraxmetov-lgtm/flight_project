from typing import Any

from loguru import logger

from app.exceptions.base import SeatTemplateNotFoundException
from app.schemas.seat_template_seats import SeatTemplateSeatCreate, SeatShortResponse, \
    SeatTemplateMapResponse
from app.services.base import BaseService
from app.helpers.seat_type import SeatType
from app.helpers.cabin_class import CabinClass
from app.services.seat_templates import SeatTemplatesService

class SeatTemplateSeatsService(BaseService):
    def generate_seat_template(self, seat_template_id: int, rows: int, business_class_rows: int) -> list[dict[str, Any]]:
        seats_to_create = []
        LETTERS: list[str] = ["A", "B", "C", "D", "E", "F"]
        for row in range(1, rows + 1):
            current_class = CabinClass.BUSINESS if row <= business_class_rows else CabinClass.ECONOMY

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
                    "seat_template_id": seat_template_id,
                    "seat_number": f"{row}{letter}",
                    "seat_type": stype,
                    "row_number": row,
                    "seat_letter": letter,
                    "cabin_class": current_class
                })
        return seats_to_create

    async def seat_template_seat_create(self, payload: SeatTemplateSeatCreate):
        if payload.seat_template_id is not None:
            await self.check_if_entity_exists(self.db.seat_templates, payload.seat_template_id, SeatTemplateNotFoundException)

        data = self.generate_seat_template(seat_template_id=payload.seat_template_id, rows=payload.rows_count, business_class_rows=payload.business_class_rows)
        await self.db.seat_template_seats.add_bulk(data)
        await self.db.commit()
        logger.info(f"Seats for template created successfully", seat_template_id=payload.seat_template_id, rows=len(data))
        return {
            "template_id": payload.seat_template_id,
            "count": len(data)
        }

    async def get_seat_template_seats(self, template_id: int):
        await SeatTemplatesService(self.db).get_seat_template_or_404(template_id)
        seats = await self.db.seat_template_seats.get_ordered_and_filters_seats(template_id)
        seat_map = {}
        for seat in seats:
            if seat is not None:
                row_key = str(seat.row_number)
                seat_map.setdefault(row_key, []).append(
                    SeatShortResponse(
                        id=seat.id,
                        no=seat.seat_number.strip(),
                        cabin_class=seat.cabin_class,
                        seat_type=seat.seat_type,
                    )
                )
        return SeatTemplateMapResponse(
            template_id=template_id,
            total_seats=len(seats),
            rows=seat_map,
        )


    async def delete_seat_template_seats(self, template_id: int) -> None:
        await SeatTemplatesService(self.db).get_seat_template_or_404(template_id)
        await self.db.seat_template_seats.delete_by_template_id(template_id)
        await self.db.commit()
        logger.info(f"All seats for template {template_id} deleted successfully")