from app.exceptions.base import SameAirportException, AirportNotFoundException, SeatTemplateNotFoundException
from app.helpers.seat_status import SeatStatus
from app.schemas.flight_instances import FlightInstanceCreate
from app.services.base import BaseService

class FlightInstancesService(BaseService):
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