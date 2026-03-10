from typing import Annotated, Optional

import jwt
from fastapi import Depends, Request, Query
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.exceptions.api import NoAccessTokenHTTPException, IncorrectTokenHTTPException, NotEnoughRightsHTTPException
from app.schemas.users import UserResponse, TokenData
from app.services.users import UsersService
from app.utils.db_manager import DBManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    async with DBManager(session_factory=AsyncSessionLocal) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]
cookie_scheme = APIKeyCookie(name="access_token", description="Введите токен или авторизуйтесь")

def get_token_from_cookie(request: Request, _=Depends(cookie_scheme)) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise NoAccessTokenHTTPException
    return token


async def get_current_user(
        db: DBDep,
        token: Annotated[str, Depends(get_token_from_cookie)]
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise IncorrectTokenHTTPException

    if username is None:
        raise IncorrectTokenHTTPException

    user = await UsersService(db).get_user_by_username(username=token_data.username)

    if user is None:
        raise IncorrectTokenHTTPException

    return user

CurrentUser = Annotated[UserResponse, Depends(get_current_user)]

async def check_if_user_is_admin(
        current_user: CurrentUser
):
    if current_user.role != "admin":
        raise NotEnoughRightsHTTPException
    return current_user

admin_only = Depends(check_if_user_is_admin)

class PaginationParams(BaseModel):
    page: Annotated[Optional[int], Query(1, ge=1)]
    per_page: Annotated[Optional[int], Query(None, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]