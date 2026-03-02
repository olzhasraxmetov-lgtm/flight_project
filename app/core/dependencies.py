from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.exceptions.api import NoAccessTokenHTTPException, IncorrectTokenHTTPException
from app.schemas.users import UserResponse, TokenData
from app.services.users import UsersService
from app.utils.db_manager import DBManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    async with DBManager(session_factory=AsyncSessionLocal) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]

def get_token_from_cookie(request: Request) -> str:
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