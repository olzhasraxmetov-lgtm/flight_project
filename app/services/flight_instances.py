from app.exceptions.base import SameAirportException, AirportNotFoundException, SeatTemplateNotFoundException, \
    FlightInstanceNotFoundException, ObjectNotFoundException
from app.helpers.seat_status import SeatStatus
from app.schemas.flight_instances import FlightInstanceCreate
from app.schemas.seat_instanes_map import SeatMapShortResponse, FlightInstanceMapResponse
from app.services.base import BaseService

class FlightInstancesService(BaseService):
    async def get_flight_instance_or_404(self, flight_instance_id: int):
        try:
            return await self.db.flight_instances.get_one_with_details(flight_instance_id)
        except ObjectNotFoundException:
            raise FlightInstanceNotFoundException()

    async def create_flight_instance(self, payload: FlightInstanceCreate):
        await self.check_if_entity_exists(self.db.airports, payload.departure_airport_id, AirportNotFoundException)
        await self.check_if_entity_exists(self.db.airports, payload.arrival_airport_id, AirportNotFoundException)

        await self.check_if_entity_exists(self.db.seat_templates, payload.seat_template_id,
                                                     SeatTemplateNotFoundException)

        if payload.departure_airport_id == payload.arrival_airport_id:
            raise SameAirportException

        flight_instance = await self.db.flight_instances.add(payload, map_res=False)
        await self.db.session.flush()

        template_seats = await self.db.seat_template_seats.get_all(
            seat_template_id=payload.seat_template_id
        )
        seats_to_create = [
            {
                "flight_instance_id": flight_instance.id,
                "seat_number": s.seat_number,
                "row_number": s.row_number,
                "seat_letter": s.seat_letter,
                "cabin_class": s.cabin_class,
                "seat_type": s.seat_type,
                "status": SeatStatus.AVAILABLE
            }
            for s in template_seats
        ]
        await self.db.seat_instances_map.add_bulk(seats_to_create)

        await self.db.session.commit()
        return await self.db.flight_instances.get_one_with_details(flight_instance.id)

    async def get_flight_instance_map(self, flight_instance_id: int):
        await self.get_flight_instance_or_404(flight_instance_id)
        seats = await self.db.seat_instances_map.get_ordered_seats_map(flight_instance_id)
        seat_map = {}
        for seat in seats:
            row_key = str(seat.row_number)
            seat_map.setdefault(row_key, []).append(
                SeatMapShortResponse(
                    id=seat.id,
                    no=seat.seat_number.strip(),
                    cabin_class=seat.cabin_class,
                    seat_type=seat.seat_type,
                    price_override=seat.price_override,
                    status=seat.status,
                )
            )
        return FlightInstanceMapResponse(
            flight_instance_id=flight_instance_id,
            total_seats=len(seats),
            rows=seat_map,
        )