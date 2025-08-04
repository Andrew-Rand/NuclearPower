import pydantic

from core.unit import BaseUnit


class BaseUnitEvet(pydantic.BaseModel):
    unit: BaseUnit

    class Config:
        arbitrary_types_allowed = True