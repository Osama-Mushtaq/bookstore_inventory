# app/schemas/book.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from bson import ObjectId
from pydantic import BaseModel, Field, GetCoreSchemaHandler, GetJsonSchemaHandler


# Custom validator for MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        from pydantic import GetCoreSchemaHandler
        from pydantic_core import core_schema

        return core_schema.general_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        from pydantic import GetJsonSchemaHandler

        json_schema = handler(schema)
        json_schema.update(type='string')
        return json_schema

class BookBase(BaseModel):
    title: str = Field(...)
    author: str = Field(...)
    genre: str = Field(...)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    publication_date: date = Field(...)
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    publication_date: Optional[date]
    description: Optional[str]

class BookInDB(BookBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        'populate_by_name': True,
        'arbitrary_types_allowed': True,
        'json_encoders': {ObjectId: str}
    }
