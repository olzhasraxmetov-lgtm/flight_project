from fastapi import status, HTTPException

class BaseAppHTTPException(HTTPException):
    """Базовый класс, который умеет хранить статус и сообщение"""
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Internal Server Error"
    log_message = None

    def __init__(self, detail: str = None, log_message: str = None):
        super().__init__(
            status_code=self.status_code,
            detail=detail or self.detail
        )
        self.detail = detail or self.detail
        self.log_message = log_message or self.detail


class IncorrectTokenHTTPException(BaseAppHTTPException):
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