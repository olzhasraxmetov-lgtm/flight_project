from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings
from app.exceptions.api import UserEmailAlreadyExistsHTTPException
from app.exceptions.base import EmailNotRegisteredException, IncorrectPasswordException, UserAlreadyExistException, \
    ObjectAlreadyExistException, UserNotFoundException
from app.schemas.users import UserRequestCreate, UserCreate, UserLoginRequest
from app.services.base import BaseService
from loguru import logger

class UsersService(BaseService):
    password_hash = PasswordHash.recommended()

    def verify_password(self,plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def create_access_token(self,data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def get_password_hash(self,password):
        return self.password_hash.hash(password)

    async def register_user(self, payload: UserRequestCreate):
        hashed_password = self.password_hash.hash(payload.password)
        new_user_data = UserCreate(**payload.model_dump(), hashed_password=hashed_password)
        try:
            new_user = await self.db.users.add(new_user_data)
            assert new_user is not None
            await self.db.commit()
            logger.info(f"New user registered successfully", user_id=new_user.id, email=new_user.email)
        except ObjectAlreadyExistException:
            raise UserEmailAlreadyExistsHTTPException
        return new_user

    async def authenticate_user(self, payload: UserLoginRequest):
        user = await self.db.users.get_user_with_hashed_password(email=payload.email)
        if not user:
            logger.warning("Login failed: email not registered", email=payload.email)
            raise EmailNotRegisteredException
        if not self.verify_password(payload.password, user.hashed_password):
            logger.warning("User login failed", user_id=user.id, reason="invalid_password")
            raise IncorrectPasswordException
        access_token = self.create_access_token({"sub": user.username})
        logger.info("User authenticated", user_id=user.id, username=user.username)
        return access_token

    async def get_user_by_username(self, username: str):
        return await self.db.users.get_one_or_none(username=username)

    async def get_my_profile(self, user_id: int):
        user_orm = await self.db.users.get_one_or_none(id=user_id, map_res=False)

        if not user_orm:
            raise UserNotFoundException

        if self.db.users.mapper is None:
            return user_orm

        return self.db.users.mapper.map_to_domain_entity(user_orm)