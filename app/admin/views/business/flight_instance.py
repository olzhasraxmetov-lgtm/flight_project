from app.models.flight_instances import FlightInstancesORM
from sqladmin import ModelView
from sqladmin.filters import ForeignKeyFilter, OperationColumnFilter, StaticValuesFilter
from app.models.seat_instances_map import SeatInstancesMapORM
from app.models import SeamTemplatesORM

class FlightInstanceAdmin(ModelView, model=FlightInstancesORM):
    column_list = [
        FlightInstancesORM.id,
        FlightInstancesORM.flight_number,
        FlightInstancesORM.status,
        FlightInstancesORM.departure_at,
        FlightInstancesORM.arrival_at,
        FlightInstancesORM.departure_airport,
        FlightInstancesORM.arrival_airport,
        FlightInstancesORM.seat_template,

    ]
    inline_models = [
        (SeatInstancesMapORM, dict(form_columns=["seat_number", "status"]))
    ]
    column_searchable_list = ["flight_number"]
    form_excluded_columns = ["passengers"]
    column_filters = [
        ForeignKeyFilter(FlightInstancesORM.seat_template_id, SeamTemplatesORM.name, title="Шаблон"),
        OperationColumnFilter(FlightInstancesORM.departure_at, title="Дата вылета"),
        OperationColumnFilter(FlightInstancesORM.arrival_at, title="Дата посадки"),
        StaticValuesFilter(
            FlightInstancesORM.flight_status_str,
            values=[
                ("SCHEDULED", "Запланировано"),
                ("DELAYED", "Перенесено"),
                ("DEPARTED", "Вылетел"),
                ("ARRIVED", "Прилетел"),
                ("CANCELLED", "Отменен"),
            ],
            title="Статус рейса"
        ),
    ]
    name = "Определенный рейс"
    name_plural = "Определенные рейсы"
    icon = "fa-solid fa-plane-arrival"