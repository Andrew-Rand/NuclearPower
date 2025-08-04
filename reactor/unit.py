import asyncio

from core.unit import BaseUnit


class Reactor(BaseUnit):
    roads_level: int
    reactivity: float
    temperature: float
    water_pressure: int
    steam_pressure: float

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
        self.reactivity = self.roads_level
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