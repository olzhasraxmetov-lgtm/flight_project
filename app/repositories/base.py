from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, Sequence, update, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import ObjectAlreadyExistException, ObjectNotFoundException
from app.mappers.base import DataMapper
from loguru import logger

class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_paginated_items(
            self,
            offset: int,
            limit: int,
            **filters
    ):
        query = select(self.model)

        if filters:
            filter_clauses = []
            for key, value in filters.items():
                if value:
                    column = getattr(self.model, key, None)
                    if column:
                        if isinstance(value, str):
                            filter_clauses.append(column.ilike(f"%{value.strip()}%"))
                        else:
                            filter_clauses.append(column == value)
            if filter_clauses:
                query = query.filter(*filter_clauses)

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel | dict):
        values = data if isinstance(data, dict) else data.model_dump()
        try:
            add_stmt = insert(self.model).values(**values).returning(self.model)
            result = await self.session.execute(add_stmt)
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            logger.warning("Integrity error", model_name=self.model.__name__, detail=str(ex))
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistException from ex
            else:
                logger.error(f"Unexpected IntegrityError: {ex}")
                raise ex

    async def add_bulk(self, data: Sequence[BaseModel | dict]):
        values = [
            item if isinstance(item, dict) else item.model_dump()
            for item in data
        ]

        try:
            add_stmt = insert(self.model).values(values).returning(self.model)
            result = await self.session.execute(add_stmt)

            models = result.scalars().all()

            return [self.mapper.map_to_domain_entity(m) for m in models]

        except IntegrityError as ex:
            logger.warning("Bulk Integrity error", model_name=self.model.__name__)
            if "unique constraint" in str(ex.orig).lower():
                raise ObjectAlreadyExistException from ex
            raise ex

    async def edit(self, data: BaseModel | dict, exclude_unset: bool = False, **filter_by) -> None:
        values = data if isinstance(data, dict) else data.model_dump(exclude_unset=exclude_unset)
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**values)
            .returning(self.model)
        )
        result = await self.session.execute(edit_stmt)
        updated_obj = result.scalar_one_or_none()

        if updated_obj is None:
            logger.warning(
                "No entity found to edit",
                model_name=self.model.__name__,
                filters=filter_by
            )
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(updated_obj)


    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        result = await self.session.execute(delete_stmt)
        deleted_id = result.scalar_one_or_none()
        if not deleted_id:
            logger.warning("No entity found to delete",model_name=self.model.__name__,filters=filter_by)
            raise ObjectNotFoundException