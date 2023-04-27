from typing import Any, AsyncIterable, Iterable

from pydantic import BaseModel


class PydanticSerializer(BaseModel):
    """
    PydanticSerializer class.

    This class is used to serialize and deserialize data.
    """

    @classmethod
    async def parse(cls, obj: Any):
        if isinstance(obj, PydanticSerializer):
            return obj
        if isinstance(obj, dict):
            return cls.parse_obj(obj)
        if isinstance(obj, AsyncIterable):
            return [cls.from_orm(obj) async for obj in obj]
        if isinstance(obj, Iterable) and not isinstance(
            obj, (str, bytes, dict, BaseModel)
        ):
            return [await cls.parse(o) for o in obj]
        else:
            return cls.from_orm(obj)

    class Config:
        """PydanticSerializer config."""

        orm_mode = True
        allow_population_by_field_name = True
        use_enum_values = True
