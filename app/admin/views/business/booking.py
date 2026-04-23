from markupsafe import Markup
from sqladmin import ModelView
from sqladmin.filters import OperationColumnFilter, StaticValuesFilter

from app.models.bookings import BookingsORM
from app.models.passengers import PassengersORM
from app.models.payments import PaymentsORM


class BookingAdmin(ModelView, model=BookingsORM):
    column_list = [
        BookingsORM.id,
        BookingsORM.booking_reference,
        BookingsORM.status,
        BookingsORM.total_price,
        BookingsORM.created_at,
        BookingsORM.user,
    ]
    form_excluded_columns = ["passengers"]
    column_default_sort = [("created_at", True)]
    column_searchable_list = ["id", "booking_reference", "user.username", "user.email"]
    column_filters = [
        OperationColumnFilter(BookingsORM.booking_reference, title="Код брони"),
        OperationColumnFilter(BookingsORM.created_at, title="Дата создания брони"),
        StaticValuesFilter(
            BookingsORM.booking_status_str,
            values=[
                ("CREATED", "Создано"),
                ("CONFIRMED", "Оплачено"),
                ("CANCELLED", "Отменено"),
            ],
            title="Статус брони"
        ),
    ]
    inline_models = [
        (PassengersORM, dict(form_columns=["first_name", "last_name", "passport_number"])),
        (PaymentsORM, dict(form_columns=["id", "amount", "status", "payment_type"])),
    ]
    column_formatters = {
        BookingsORM.status: lambda m, a: Markup(
            f'<span class="badge '
            f'{"bg-success" if m.status.value == "confirmed" else "bg-warning" if m.status.value == "created" else "bg-danger"}">'
            f'{m.status.value}</span>'
        )
    }
    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-plane"
    can_create = False