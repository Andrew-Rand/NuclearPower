from pydantic import BaseModel


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


class SetRoadsLevelRequest(BaseModel):
    level: int


class SetRoadsLevelResponse(BaseModel):
    info: str
    current_level: int
