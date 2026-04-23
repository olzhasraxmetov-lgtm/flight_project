from typing import Any

from sqladmin import ModelView
from sqladmin.filters import StaticValuesFilter
from starlette.requests import Request
from wtforms import SelectField, PasswordField
from app.services.users import UsersService
from app.models import UsersORM


class UserAdmin(ModelView, model=UsersORM):
    column_list = [UsersORM.id, UsersORM.email, UsersORM.username, UsersORM.phone, UsersORM.role]
    column_searchable_list = ["email", "username", "phone"]
    column_filters = [
        StaticValuesFilter(
            UsersORM.user_role_str,
            values=[
                ("user", "Пользователь"),
                ("admin", "Админ"),
            ],
            title="Роль"
        ),
    ]
    form_columns = ["email", "username", "phone", "hashed_password","role"]
    form_extra_fields = {
        "password": PasswordField("Пароль")
    }
    form_overrides = {
        "role": SelectField,
        "hashed_password": PasswordField
    }
    form_args = {
        "role": {
            "choices": [
                ("user", "Пользователь"),
                ("admin", "Администратор"),
            ]
        },
        "hashed_password": {"label": "Пароль"}
    }

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        password = data.get("password")
        if password:
            model.hashed_password = UsersService().get_password_hash(password)

        if "password" in data:
            del data["password"]