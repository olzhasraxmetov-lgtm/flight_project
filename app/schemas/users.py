from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator
import re
from app.helpers.users_role import UserRoleEnum


class UserBase(BaseModel):
    email: EmailStr = Field(min_length=7, max_length=30, description='Почта пользователя')
    username: str = Field(min_length=6, max_length=15, description='Имя пользователя')
    phone: str = Field(description='Телефон пользователя')

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        clean_phone = re.sub(r"[^\d+]", "", v)

        if not re.match(r"^\+7\d{10}$", clean_phone):
            raise ValueError("Номер телефона должен быть в формате +77022955423")

        return clean_phone

class UserRequestCreate(UserBase):
    password: str

class UserCreate(UserBase):
    hashed_password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRoleEnum = UserRoleEnum.USER
    created_at: datetime

class UserWithHashedPassword(UserBase):
    id: int
    hashed_password: str

class TokenData(BaseModel):
    username: str | None = None