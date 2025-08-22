import asyncio

from constants import ROADS_ENDS_EFFECT
from core.unit import BaseUnit
from station.reactor.schemas import WarningEvent, CriticalEvent


class Reactor(BaseUnit):
    roads_level: int
    reactivity: float
    temperature: float
    water_pressure: int
    steam_pressure: float

    xenon_level: float
    road_ends_effect: float

    current_task: asyncio.Task | None

    warnings = list[WarningEvent]
    critical = list[CriticalEvent]

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
        self._roads_level = roads_level
        self.reactivity = reactivity
        self.temperature = temperature
        self._water_pressure = water_pressure
        self.steam_pressure = steam_pressure

        self.xenon_level = 0
        self.road_ends_effect = 0

        self.warnings = []
        self.critical = []

        self.current_roads_task = None
        self.current_water_task = None

    @property
    def roads_level(self) -> int:
        return self._roads_level

    @roads_level.setter
    def roads_level(self, roads_level: int):
        self._roads_level = roads_level


    @property
    def water_pressure(self) -> int:
        return self._water_pressure

    @water_pressure.setter
    def water_pressure(self, water_pressure: int):
        self._water_pressure = water_pressure

    @property
    def conditions(self) -> dict[str, int | float]:
        return {
            'roads_level': self.roads_level,
            'reactivity': self.reactivity,
            'temperature': self.temperature,
            'water_pressure': self.water_pressure,
            'steam_pressure': self.steam_pressure,
            'xenon_level': self.xenon_level,
            'warnings': self.warnings,
            'critical': self.critical,
        }


    def check_warnings(self):
        # need to check already added and remove if all good
        # create events
        pass


    def check_critical(self):
        # do not return critical
        # its over
        pass


    async def update_conditions(self):
        self.reactivity = self.roads_level * 10 - self.xenon_level + self.road_ends_effect * self.roads_level

        temperature_factor = self.reactivity - self.water_pressure
        if self.temperature + temperature_factor < 0:
            self.temperature = 0
        else:
            self.temperature += temperature_factor
        self.steam_pressure = self.temperature * (self.water_pressure / 10)

        self.check_warnings()
        self.check_critical()

        print(f'Level: {self.roads_level}, Reactivity: {self.reactivity}, Temperature: {self.temperature}, Water pressure: {self.water_pressure}, Steam pressure: {self.steam_pressure}')

    async def tick(self):
        while True:
            await asyncio.sleep(1)
            await self.update_conditions()

    async def _set_roads_level(self, level: int):
        if any([self.roads_level == level, self.roads_level < 0, self.roads_level > 10]):
            return
        while self.roads_level != level:
            await asyncio.sleep(1)
            if self.roads_level < level:
                self.roads_level += 1
            else:
                self.roads_level -= 1

    async def _set_water_level(self, level: int):
        if any([self.water_pressure == level, self.water_pressure < 1, self.water_pressure > 100]):
            return
        while self.water_pressure != level:
            await asyncio.sleep(0.5)
            if self.water_pressure < level:
                self.water_pressure += 1
            else:
                self.water_pressure -= 1

    async def set_roads_level(self, roads_level: int):
        if self.current_roads_task is not None and not self.current_roads_task.done():
            self.current_roads_task.cancel()

        self.current_roads_task = asyncio.create_task(self._set_roads_level(roads_level))

    async def set_water_level(self, water_level: int):
        if self.current_water_task is not None and not self.current_water_task.done():
            self.current_water_task.cancel()

        self.current_water_task = asyncio.create_task(self._set_water_level(water_level))


    async def increase_reactivity(self, percent: int):
        self.reactivity += self.reactivity * (percent / 100)

    async def az_5_shut_down(self):
        """First to seconds it increases reactivity"""
        await self.set_roads_level(0)
        self.road_ends_effect = ROADS_ENDS_EFFECT

        await asyncio.sleep(2)
        self.road_ends_effect = 0