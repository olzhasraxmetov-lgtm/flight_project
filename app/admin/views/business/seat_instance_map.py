from markupsafe import Markup

from app.models import FlightInstancesORM
from app.models.seat_instances_map import SeatInstancesMapORM
from sqladmin import ModelView
from sqladmin.filters import ForeignKeyFilter, StaticValuesFilter

class SeatInstanceMapAdmin(ModelView, model=SeatInstancesMapORM):
    column_list = [
        SeatInstancesMapORM.id,
        SeatInstancesMapORM.seat_number,
        SeatInstancesMapORM.cabin_class,
        SeatInstancesMapORM.seat_type,
        SeatInstancesMapORM.row_number,
        SeatInstancesMapORM.seat_letter,
        SeatInstancesMapORM.status
    ]
    column_searchable_list = ["seat_number"]
    column_default_sort = [("flight_instance_id", False), ("row_number", False)]
    column_filters = [
        ForeignKeyFilter(SeatInstancesMapORM.flight_instance_id, FlightInstancesORM.id, title="Рейс (ID)"),
        StaticValuesFilter(
            SeatInstancesMapORM.status_str,
            values=[
                ("AVAILABLE", "Доступно"),
                ("RESERVED", "Забронировано"),
                ("SOLD", "Продано"),
                ("BLOCKED", "Недоступно"),
                ("CHECKED_IN", "Оплачено"),
            ],
            title="Статус места"
        )
    ]
    column_formatters = {
        SeatInstancesMapORM.status: lambda m, a: Markup(
            f'<span class="badge {"bg-success" if m.status.value == "available" else "bg-danger"}">{m.status.value}</span>'
        )
    }
    name = "Место для рейса"
    name_plural = "Места для рейса"
    icon = "fa-solid fa-couch"