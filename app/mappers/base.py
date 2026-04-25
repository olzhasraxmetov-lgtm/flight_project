from typing import TypeVar, Type, Generic, Any

from pydantic import BaseModel

from app.core.database import Base

SchemaType = TypeVar('SchemaType', bound=BaseModel)
DBModelType = TypeVar('DBModelType', bound=Base)

class DataMapper(Generic[DBModelType, SchemaType]):
    db_model: Type[DBModelType] | None = None
    schema: Type[SchemaType] | None = None

    @classmethod
    def map_to_domain_entity(cls, db_model: DBModelType) -> SchemaType:
        if cls.schema is None:
            raise ValueError(f"Schema is not defined for {cls.__name__}")

        return cls.schema.model_validate(db_model, from_attributes=True)

    @classmethod
    def map_to_persistent_entity(cls, data: Any) -> DBModelType:
        if cls.db_model is None:
            raise ValueError(f"db_model is not defined for {cls.__name__}")

        return cls.db_model(**data.model_dump())