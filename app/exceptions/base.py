class AppBaseException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(AppBaseException):
    detail = "Объект не найден"

class ObjectAlreadyExistException(AppBaseException):
    detail = "Похожий объект уже существует"

class EmailNotRegisteredException(AppBaseException):
    detail = "Пользователь с таким email не зарегистрирован"

class UserAlreadyExistException(AppBaseException):
    detail = 'Пользователь уже существует'

class IncorrectPasswordException(AppBaseException):
    detail = 'Неверный пароль'