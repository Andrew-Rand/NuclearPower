import asyncio

from constants import ROADS_ENDS_EFFECT
from core.unit import BaseUnit


class Reactor(BaseUnit):
    roads_level: int
    reactivity: float
    temperature: float
    water_pressure: int
    steam_pressure: float

    xenon_level: float
    road_ends_effect: float

    current_task: asyncio.Task | None

    # TODO: time after refuel (reactivity decrease)
    # TODO: ksenon (reactivity decrease)


    def __init__(
            self,
            roads_level: int = 0,
            reactivity: float = 0,
            temperature: float = 0,
            water_pressure: int = 1,
            steam_pressure: float = 0,
    ):
        self.roads_level = roads_level
        self.reactivity = reactivity
        self.temperature = temperature
        self.water_pressure = water_pressure
        self.steam_pressure = steam_pressure

        self.xenon_level = 0
        self.road_ends_effect = 0

        self.current_task = None


    @property
    def conditions(self) -> dict[str, int | float]:
        return {
            'roads_level': self.roads_level,
            'reactivity': self.reactivity,
            'temperature': self.temperature,
            'water_pressure': self.water_pressure,
            'steam_pressure': self.steam_pressure,
        }

    async def update_conditions(self):
        self.reactivity = self.roads_level * 10 - self.xenon_level + self.road_ends_effect
        temperature_factor = self.reactivity - self.water_pressure / 100
        if self.temperature + temperature_factor < 0:
            self.temperature = 0
        else:
            self.temperature += temperature_factor
        self.steam_pressure = self.temperature * self.water_pressure

        print(f'Level: {self.roads_level}, Reactivity: {self.reactivity}, Temperature: {self.temperature}, Steam pressure: {self.steam_pressure}')

    async def tick(self):
        while True:
            await asyncio.sleep(1)
            await self.update_conditions()

    async def _set_roads_level(self, roads_level: int):
        if self.roads_level == roads_level:
            return
        while self.roads_level != roads_level:
            await asyncio.sleep(1)
            if self.roads_level < roads_level:
                self.roads_level += 1
            else:
                self.roads_level -= 1

    async def set_roads_level(self, roads_level: int):
        if self.current_task is not None and not self.current_task.done():
            self.current_task.cancel()


        self.current_task = asyncio.create_task(self._set_roads_level(roads_level))


    async def increase_reactivity(self, percent: int):
        self.reactivity += self.reactivity * (percent / 100)

    async def az_5_shut_down(self):
        """First to seconds it increases reactivity"""
        await self.set_roads_level(0)
        self.road_ends_effect = ROADS_ENDS_EFFECT

        await asyncio.sleep(2)
        self.road_ends_effect = 0