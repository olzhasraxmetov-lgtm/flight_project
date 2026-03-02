from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings
from app.exceptions.base import EmailNotRegisteredException, IncorrectPasswordException
from app.schemas.users import UserRequestCreate, UserCreate, UserLoginRequest
from app.services.base import BaseService


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
        new_user = await self.db.users.add(new_user_data)
        await self.db.commit()
        return new_user

    async def authenticate_user(self, payload: UserLoginRequest):
        user = await self.db.users.get_user_with_hashed_password(email=payload.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(payload.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"sub": user.username})
        return access_token

    async def get_user_by_username(self, username: str):
        return await self.db.users.get_one_or_none(username=username)

    async def get_my_profile(self):
        return await self.db.users.mapper.map_to_domain_entity()