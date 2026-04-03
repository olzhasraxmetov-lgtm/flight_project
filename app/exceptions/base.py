class AppBaseException(Exception):
    detail = "Непредвиденная ошибка"
    status_code = 500

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ForbiddenBookingException(AppBaseException):
    detail = "У вас нет прав для редактирования этого бронирования"
    status_code = 403

class ObjectNotFoundException(AppBaseException):
    detail = "Объект не найден"
    status_code = 404

class ObjectAlreadyExistException(AppBaseException):
    detail = "Похожий объект уже существует"
    status_code = 409

class EmailNotRegisteredException(AppBaseException):
    detail = "Пользователь с таким email не зарегистрирован"
    status_code = 401

class UserAlreadyExistException(AppBaseException):
    detail = 'Пользователь уже существует'
    status_code = 409

class IncorrectPasswordException(AppBaseException):
    detail = 'Неверный пароль'
    status_code = 401

class AirlineNotFoundException(ObjectNotFoundException):
    detail = 'Авиакомпания не найдена'

class AirportNotFoundException(ObjectNotFoundException):
    detail = 'Аэропорт не найден'

class FlightNotFoundException(ObjectNotFoundException):
    detail = 'Рейс не найден'

class AircraftNotFoundException(ObjectNotFoundException):
    detail = 'Самолет не найден'

class SeatTemplateNotFoundException(ObjectNotFoundException):
    detail = 'Шаблон самолета не найден'

class FlightInstanceNotFoundException(ObjectNotFoundException):
    detail = 'Рейс не найден'

class BookingNotFoundException(ObjectNotFoundException):
    detail = 'Бронирование не найдено'

class PassengerNotFoundException(ObjectNotFoundException):
    detail = 'Пассажир не найде'

class SameAirportException(AppBaseException):
    status_code = 400
    detail = 'Аэропорт вылета не может быть аэропортом прилета'

class FlightNotAvailableForBookingException(AppBaseException):
    status_code = 409
    detail = "Рейс уже вылетел или отменен"

class SeatsNotAvailableException(AppBaseException):
    status_code = 409
    detail = "Место уже занято или недоступно"