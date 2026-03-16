from datetime import datetime

from app.exceptions.api import InvalidDateTimeException
from app.exceptions.base import ObjectNotFoundException
from app.utils.db_manager import DBManager
from app.exceptions.base import AppBaseException
from loguru import logger

class BaseService:
    db: DBManager | None

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db


    async def check_if_entity_exists(self, repo, entity_id: id, error_exception: type[AppBaseException]):
        """
            Универсальный метод проверки существования сущности.
            :param repo: Репозиторий (например, self.db.airports)
            :param entity_id: ID сущности
            :param error_exception: Класс исключения, которое нужно выбросить
        """
        try:
            entity = await repo.get_one(id=entity_id)
        except ObjectNotFoundException as ex:
            entity_name = error_exception.__name__.replace("NotFoundException", "")
            logger.warning(f"{entity_name} not found", entity_id=entity_id)
            raise error_exception from ex
        return entity

    @staticmethod
    def check_date_to_after_date_from(departure_at: datetime, arrival_at: datetime) -> None:
        if departure_at >= arrival_at:
            raise InvalidDateTimeException