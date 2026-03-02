from fastapi import APIRouter, Body
from app.core.dependencies import DBDep
from app.exceptions.base import ObjectAlreadyExistException
from app.exceptions.api import UserEmailAlreadyExistsHTTPException
from app.schemas.users import UserRequestCreate
from app.services.users import UsersService
router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.post("", summary='Регистрация нового пользователя')
async def create_user(
    db: DBDep,
    payload: UserRequestCreate = Body(...),
):
    try:
        return await UsersService(db).register_user(payload)
    except ObjectAlreadyExistException:
        raise UserEmailAlreadyExistsHTTPException