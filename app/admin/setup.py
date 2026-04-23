from sqladmin import Admin

from app.admin.auth import AdminAuth
from app.admin.views.business.booking import BookingAdmin
from app.admin.views.business.payment import PaymentAdmin
from app.admin.views.business.passenger import PassengerAdmin
from app.admin.views.business.seat_instance_map import SeatInstanceMapAdmin
from app.admin.views.business.flight_instance import FlightInstanceAdmin
from app.admin.views.references import AirportAdmin, AirlineAdmin, AircraftAdmin, FlightAdmin, SeatTemplateAdmin, \
    SeatTemplateSeatsAdmin
from app.admin.views.users import UserAdmin
from app.core.config import settings

authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)

def setup_admin(app, engine):
    admin = Admin(
        app,
        engine,
        authentication_backend=authentication_backend,
        title="Flight System Admin"
    )
    views = [
        BookingAdmin, FlightInstanceAdmin, PaymentAdmin, PassengerAdmin, SeatInstanceMapAdmin,
        UserAdmin,
        AirportAdmin, AirlineAdmin, AircraftAdmin,FlightAdmin,SeatTemplateAdmin,SeatTemplateSeatsAdmin,
    ]

    for view in views:
        admin.add_view(view)