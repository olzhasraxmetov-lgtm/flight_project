from typing import Sequence, cast

from sqlalchemy.orm import joinedload

from app.exceptions.base import (AirportNotFoundException, AirlineNotFoundException,
                                 SameAirportException, FlightNotFoundException, ObjectNotFoundException)
from app.schemas.flights import FlightCreate, FlightResponse, FlightResponseWithoutRels, FlightUpdate, FlightSearch
from app.services.base import BaseService
from loguru import logger

class FlightsService(BaseService):

    async def get_flight_or_404(self, flight_id: int):
        try:
            return await self.db.flights.get_one(id=flight_id, map_res=False)
        except ObjectNotFoundException:
            logger.warning("Flight not found", flight_id=flight_id)
            raise FlightNotFoundException

    async def get_paginated_flights(
            self,
            search: FlightSearch,
            pagination
    ) -> Sequence[FlightResponse]:
        filter_clauses = []
        options = [
            joinedload(self.db.flights.model.airline),
            joinedload(self.db.flights.model.departure_airport),
            joinedload(self.db.flights.model.arrival_airport),
        ]
        if search.date_from:
            filter_clauses.append(self.db.flights.model.departure_at >= search.date_from)

        if search.date_to:
            filter_clauses.append(self.db.flights.model.departure_at <= search.date_to)

        if search.max_price and search.max_price > 0:
            filter_clauses.append(self.db.flights.model.price <= search.max_price)

        result =  await self.db.flights.get_paginated_items(
            *filter_clauses,
            offset=(pagination.page - 1) * (pagination.per_page or 5),
            limit=pagination.per_page or 5,
            options=options,
            departure_airport_id=search.departure_airport_id,
            arrival_airport_id=search.arrival_airport_id,
            airline_id=search.airline_id,
        )
        return cast(Sequence[FlightResponse], result)

    async def _validation_for_entities(self, payload: FlightCreate | FlightUpdate) -> None:
        if payload.departure_airport_id is not None:
            await self.check_if_entity_exists(self.db.airports, payload.departure_airport_id,
                                              error_exception=AirportNotFoundException)
        if payload.arrival_airport_id is not None:
            await self.check_if_entity_exists(self.db.airports, payload.arrival_airport_id,
                                              error_exception=AirportNotFoundException)
        if payload.airline_id is not None:
            await self.check_if_entity_exists(self.db.airlines, payload.airline_id,
                                              error_exception=AirlineNotFoundException)


    async def create_flight(self, payload: FlightCreate) -> FlightResponse:
        await self._validation_for_entities(payload)

        self.check_date_to_after_date_from(payload.departure_at, payload.arrival_at)

        if payload.departure_airport_id == payload.arrival_airport_id:
            raise SameAirportException


        new_flight = await self.db.flights.add(payload, map_res=False)
        assert new_flight is not None
        await self.db.commit()
        logger.info(f"Flight created successfully",
                    updated_data=payload.model_dump(exclude_unset=True, mode="json"))
        flight_response = await self.db.flights.get_flight_with_rels(new_flight.id)
        if not flight_response:
            raise FlightNotFoundException

        return flight_response

    async def get_flight(self, flight_id: int) -> FlightResponse:
        flight = await self.db.flights.get_flight_with_rels(flight_id)
        if not flight:
            raise FlightNotFoundException
        return flight

    async def delete_flight(self, flight_id: int) -> None:
        await self.get_flight_or_404(flight_id)

        await self.db.flights.delete(id=flight_id)
        await self.db.commit()
        logger.info(f"Flight deleted successfully", flight_id=flight_id)

    async def _edit_flight(self, flight_id: int, payload: FlightUpdate, exclude_unset) -> FlightResponseWithoutRels:
        await self.get_flight_or_404(flight_id)
        await self._validation_for_entities(payload)
        updated_flight = await self.db.flights.edit(id=flight_id, data=payload, map_res=False, exclude_unset=exclude_unset)
        if not updated_flight:
            raise ObjectNotFoundException
        await self.db.commit()
        logger.info(f"Flight updated successfully", flight_id=flight_id,
                    updated_data=payload.model_dump(exclude_unset=True, mode="json"))

        return updated_flight

    async def update_flight(self, payload: FlightUpdate, flight_id: int) -> FlightResponseWithoutRels:
        return await self._edit_flight(payload=payload, flight_id=flight_id, exclude_unset=False)

    async def partially_update_flight(self, payload: FlightUpdate, flight_id: int) -> FlightResponseWithoutRels:
        return await self._edit_flight(payload=payload, flight_id=flight_id, exclude_unset=True)
