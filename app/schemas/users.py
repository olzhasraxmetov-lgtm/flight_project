from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.helpers.users_role import UserRoleEnum


class UserBase(BaseModel):
    email: EmailStr = Field(min_length=7, max_length=30, description='Почта пользователя')
    username: str = Field(min_length=6, max_length=15, description='Имя пользователя')
    phone: PhoneNumber = Field(description='Телефон пользователя')

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