from fastapi import APIRouter

from station.reactor.schemas import ReactorConditionsResponse, SetRoadsLevelRequest, SetRoadsLevelResponse
from main import station


reactor_router = APIRouter(prefix='/reactor')


@reactor_router.get('/conditions', response_model=ReactorConditionsResponse)
async def get_reactor_conditions():
    return station.reactor.conditions


@reactor_router.get('/az-5', response_model=SetRoadsLevelResponse)
async def get_reactor_conditions():
    await station.reactor.az_5_shut_down()
    return {'info': 'az-5 activated', 'current_level': station.reactor.roads_level}


@reactor_router.post('/roads-level', response_model=SetRoadsLevelResponse)
async def set_road_level(data: SetRoadsLevelRequest):
    await station.reactor.set_roads_level(data.level)
    return {'info': 'ok', 'current_level': station.reactor.roads_level}