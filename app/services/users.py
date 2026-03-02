from datetime import datetime, timedelta, timezone

from app.services.base import BaseService
from pwdlib import PasswordHash
from app.core.config import settings
from app.schemas.users import UserRequestCreate, UserCreate
import jwt

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