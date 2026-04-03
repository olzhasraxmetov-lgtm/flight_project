from datetime import datetime, time

from sqlalchemy.orm import joinedload
import zoneinfo
from app.exceptions.base import SameAirportException, AirportNotFoundException, SeatTemplateNotFoundException, \
    FlightInstanceNotFoundException, ObjectNotFoundException
from app.helpers.flight_status import FlightStatus
from app.helpers.seat_status import SeatStatus
from app.schemas.flight_instances import FlightInstanceCreate, FlightInstanceStatusUpdate, FlightInstanceResponse
from app.schemas.flights import FlightSearch
from app.schemas.seat_instanes_map import SeatMapShortResponse, FlightInstanceMapResponse
from app.services.base import BaseService

class FlightInstancesService(BaseService):
    async def validate_flight_for_booking(self, flight_instance_id: int):
        flight = await self.db.flight_instances.get_one_or_none(id=flight_instance_id, map_res=False)
        if not flight:
            raise FlightInstanceNotFoundException()
        return flight

    async def get_flight_instance_or_404(self, flight_instance_id: int):
        try:
            return await self.db.flight_instances.get_one_with_details(flight_instance_id)
        except ObjectNotFoundException:
            raise FlightInstanceNotFoundException()

    async def get_paginated_flight_instances(
            self,
            search: FlightSearch,
            pagination
    ) -> list[FlightInstanceResponse]:
        filter_clauses = []

        search_tz = zoneinfo.ZoneInfo("UTC")

        options = [
            joinedload(self.db.flight_instances.model.departure_airport),
            joinedload(self.db.flight_instances.model.arrival_airport),
        ]

        if search.departure_airport_id:
            airport = await self.db.airports.get_one(id=search.departure_airport_id)
            if airport:
                search_tz = zoneinfo.ZoneInfo(airport.timezone)

        if search.date_from:
            local_start = datetime.combine(search.date_from.date(), time.min).replace(tzinfo=search_tz)
            filter_clauses.append(
                self.db.flight_instances.model.departure_at >= local_start.astimezone(zoneinfo.ZoneInfo("UTC"))
            )

        if search.date_to:
            local_end = datetime.combine(search.date_to.date(), time.max).replace(tzinfo=search_tz)
            filter_clauses.append(
                self.db.flight_instances.model.departure_at <= local_end.astimezone(zoneinfo.ZoneInfo("UTC"))
            )


        if search.max_price and search.max_price > 0:
            filter_clauses.append(self.db.flight_instances.model.base_price <= search.max_price)

        filter_clauses.append(self.db.flight_instances.model.status == FlightStatus.SCHEDULED)

        return await self.db.flight_instances.get_paginated_items(
            *filter_clauses,
            offset=(pagination.page - 1) * (pagination.per_page or 5),
            limit=pagination.per_page or 5,
            options=options,
            departure_airport_id=search.departure_airport_id,
            arrival_airport_id=search.arrival_airport_id,
        )

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

    async def change_flight_instance_status(self, payload: FlightInstanceStatusUpdate, flight_instance_id: int):
        try:
            await self.db.flight_instances.edit(data=payload, id=flight_instance_id, map_res=False)
            await self.db.session.commit()
            return await self.get_flight_instance_or_404(flight_instance_id)

        except ObjectNotFoundException:
            raise FlightInstanceNotFoundException()