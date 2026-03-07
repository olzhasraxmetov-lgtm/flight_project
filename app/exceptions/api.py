from fastapi import HTTPException

class BaseAppHTTPException(HTTPException):
    """Базовый класс, который умеет хранить статус и сообщение"""
    status_code = 500
    detail = "Internal Server Error"
    log_level = "ERROR"

    def __init__(self, detail: str = None, log_message: str = None, log_level: str = None, **kwargs):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)
        self.detail = detail or self.detail
        self.log_message = log_message or self.detail
        self.log_level = log_level or self.log_level
        self.extra = kwargs

class IncorrectTokenHTTPException(BaseAppHTTPException):
    status_code = 401
    detail = "Некорректный токен"

class EmailNotRegisteredHTTPException(BaseAppHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"

class UserEmailAlreadyExistsHTTPException(BaseAppHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class IncorrectPasswordHTTPException(BaseAppHTTPException):
    status_code = 401
    detail = "Пароль неверный"

class NoAccessTokenHTTPException(BaseAppHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"

class NotEnoughRightsHTTPException(BaseAppHTTPException):
    status_code = 403
    detail = "Недостаточно прав"