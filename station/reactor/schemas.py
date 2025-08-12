from pydantic import BaseModel


class ReactorConditionsResponse(BaseModel):
    roads_level: int
    reactivity: float
    temperature: float
    water_pressure: int
    steam_pressure: float


class SetRoadsLevelRequest(BaseModel):
    level: int


class SetRoadsLevelResponse(BaseModel):
    info: str
    current_level: int
