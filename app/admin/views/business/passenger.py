from sqladmin import ModelView
from app.models.passengers import PassengersORM
from app.models.bookings import BookingsORM

class PassengerAdmin(ModelView, model=PassengersORM):
    column_list = [PassengersORM.id, PassengersORM.first_name, PassengersORM.last_name]
    column_searchable_list = ["first_name", "last_name"]
    column_default_sort = [("last_name", False)]
    inline_models = [
        (BookingsORM, dict(form_columns=["id", "flight_instance_id", "status"]))
    ]
    name = "Пассажир"
    name_plural = "Пассажиры"
    icon = "fa-solid fa-passport"