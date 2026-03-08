from fastapi import APIRouter, Body, Response

from app.core.dependencies import CurrentUser
from app.core.dependencies import DBDep
from app.exceptions.api import UserEmailAlreadyExistsHTTPException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordHTTPException
from app.exceptions.base import ObjectAlreadyExistException, EmailNotRegisteredException, IncorrectPasswordException
from app.schemas.users import UserRequestCreate, UserLoginRequest
from app.services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.post("/register", summary='Регистрация нового пользователя')
async def create_user(
    db: DBDep,
    payload: UserRequestCreate = Body(...),
):
    try:
        return await UsersService(db).register_user(payload)
    except ObjectAlreadyExistException:
        raise UserEmailAlreadyExistsHTTPException

@router.post("/login", summary='Аутентификация пользователя')
async def login_user(
    db: DBDep,
    response: Response,
    payload: UserLoginRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Пользователь olzhas",
                "value": {
                    "email": "olzhas@example.com",
                    "password": "olzhas123",
                },
            },
            "2": {
                "summary": "Админ",
                "value": {
                    "email": "admin@example.com",
                    "password": "admin123",
                },
            },
        }
    ),
):
    try:
        access_token = await UsersService(db).authenticate_user(payload)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.post("/logout", summary='Выход из аккаунта')
async def logout_user(
        response: Response,
        user: CurrentUser,
):
    response.delete_cookie("access_token")
    return {"status": "success"}

@router.get("/me", summary='Мой профиль')
async def logout_user(
        user: CurrentUser,
):
    return user