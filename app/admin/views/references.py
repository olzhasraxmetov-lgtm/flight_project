from sqladmin import ModelView

from app.models import SeatTemplateSeatsORM
from app.models.airports import AirportsORM
from app.models.airlines import AirlinesORM
from app.models.aircrafts import AircraftsORM
from app.models.flights import FlightsORM
from app.models.seat_templates import SeamTemplatesORM
from sqladmin.filters import ForeignKeyFilter, OperationColumnFilter, BooleanFilter, StaticValuesFilter

class AirportAdmin(ModelView, model=AirportsORM):
    column_list = [AirportsORM.id, AirportsORM.code, AirportsORM.name, AirportsORM.city, AirportsORM.country]
    column_searchable_list = ["code", "city", "name"]
    column_filters = [
        OperationColumnFilter(AirportsORM.name),
        OperationColumnFilter(AirportsORM.city),
        OperationColumnFilter(AirportsORM.country),
    ]
    form_excluded_columns = [
        "departing_flights",
        "arrival_flights",
        "departing_instances",
        "arrival_instances"
    ]
    name = "Аэропорт"
    name_plural = "Аэропорты"
    icon = "fa-solid fa-building-columns"

class AirlineAdmin(ModelView, model=AirlinesORM):
    column_list = [AirlinesORM.id, AirlinesORM.iata_code, AirlinesORM.name]
    column_searchable_list = ["iata_code", "name"]
    column_filters = [
        OperationColumnFilter(AirlinesORM.iata_code),
        OperationColumnFilter(AirlinesORM.name),
    ]
    form_excluded_columns = ["flights"]
    name = "Авиакомпания"
    name_plural = "Авиакомпаний"
    icon = "fa-solid fa-tower-cell"

class AircraftAdmin(ModelView, model=AircraftsORM):
    column_list = [AircraftsORM.id, AircraftsORM.name, AircraftsORM.manufacturer]
    column_searchable_list = ["manufacturer", "name"]
    column_filters = [
        OperationColumnFilter(AircraftsORM.name),
        OperationColumnFilter(AircraftsORM.manufacturer),
    ]
    form_excluded_columns = ["templates"]
    name = "Самолет"
    name_plural = "Самолеты"
    icon = "fa-solid fa-plane-up"

class FlightAdmin(ModelView, model=FlightsORM):
    column_list = [
        FlightsORM.id,
        FlightsORM.flight_number,
        FlightsORM.departure_airport,
        FlightsORM.arrival_airport,
        FlightsORM.price,
        FlightsORM.airline
    ]
    column_searchable_list = ["flight_number"]
    column_filters = [
        ForeignKeyFilter(FlightsORM.airline_id, AirlinesORM.name, title="Авиакомпания"),
        OperationColumnFilter(FlightsORM.departure_at),
        OperationColumnFilter(FlightsORM.arrival_at),
        OperationColumnFilter(FlightsORM.price)
    ]
    name = "Рейс"
    name_plural = "Рейсы"
    icon = "fa-solid fa-route"

class SeatTemplateAdmin(ModelView, model=SeamTemplatesORM):
    column_list = [
        SeamTemplatesORM.id,
        SeamTemplatesORM.name,
        SeamTemplatesORM.aircraft,
        SeamTemplatesORM.is_active,
    ]
    column_default_sort = [("aircraft_model_id", False), ("name", False)]
    column_searchable_list = ["name"]
    column_filters = [
        ForeignKeyFilter(SeamTemplatesORM.aircraft_model_id, AircraftsORM.name, title="Самолет"),
        BooleanFilter(SeamTemplatesORM.is_active),
    ]
    name = "Шаблон места"
    name_plural = "Шаблоны мест"
    icon = "fa-solid fa-couch"


class SeatTemplateSeatsAdmin(ModelView, model=SeatTemplateSeatsORM):
    column_list = [
        SeatTemplateSeatsORM.id,
        SeatTemplateSeatsORM.template,
        SeatTemplateSeatsORM.seat_number,
        SeatTemplateSeatsORM.cabin_class,
        SeatTemplateSeatsORM.seat_type,
    ]

    column_default_sort = [("seat_template_id", False), ("row_number", False)]

    column_searchable_list = ["seat_number"]

    column_filters = [
        ForeignKeyFilter(SeatTemplateSeatsORM.seat_template_id, SeamTemplatesORM.name, title="Шаблон"),
        StaticValuesFilter(
            SeatTemplateSeatsORM.cabin_class_str,
            values=[
                ("ECONOMY", "Эконом"),
                ("BUSINESS", "Бизнес"),
            ],
            title="Класс места"
        ),
        StaticValuesFilter(
            SeatTemplateSeatsORM.seat_type_str,
            values=[
                ("WINDOW", "У окна"),
                ("AISLE", "У прохода"),
                ("MIDDLE", "Среднее место "),
                ("EXTRA_LEGROOM", "Доп. место для ног"),
            ],
            title="Тип места"
        ),
    ]

    name = "Место в шаблоне"
    name_plural = "Места (детали шаблонов)"
    icon = "fa-solid fa-chair"