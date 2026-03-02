from typing import TypeVar

from pydantic import BaseModel

from app.core.database import Base

SchemaType = TypeVar('SchemaType', bound=BaseModel)
DBModelType = TypeVar('DBModelType', bound=Base)

class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, db_model):
        return cls.schema.model_validate(db_model, from_attributes=True)

    @classmethod
    def map_to_persistent_entity(cls, data):
        return cls.db_model(**data.model_dump())