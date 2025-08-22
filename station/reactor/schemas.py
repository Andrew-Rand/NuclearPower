from pydantic import BaseModel, field_validator


class WarningEvent(BaseModel):
    code: int
    info: str


class CriticalEvent(WarningEvent):
    ...


class ReactorConditionsResponse(BaseModel):
    roads_level: int
    reactivity: float
    temperature: float
    water_pressure: int
    steam_pressure: float
    xenon_level: float
    warnings: list[WarningEvent]
    critical: list[CriticalEvent]


class BaseSetLevelRequest(BaseModel):
    level: int


class SetRoadsLevelRequest(BaseSetLevelRequest):
    @field_validator('level')
    def validate_level(cls, value):
        if value < 0 or value > 10:
            raise ValueError('Roads level must be between 0 and 10')
        return value


class SetWaterLevelRequest(BaseSetLevelRequest):
    @field_validator('level')
    def validate_level(cls, value):
        if value < 1 or value > 100:
            raise ValueError('Water pressure must be between 1 and 100')
        return value


class BaseLevelResponse(BaseModel):
    info: str
    current_level: int

class SetRoadsLevelResponse(BaseLevelResponse):
    ...


class SetWaterLevelResponse(BaseLevelResponse):
    ...

