import asyncio

from core.unit import BaseUnit
from station.reactor.reactor import Reactor


class Station(BaseUnit):
    reactor: Reactor

    def __init__(self, reactor: Reactor):
        self.reactor = reactor

    @property
    def conditions(self) -> dict[str, int | float]:
        pass

    async def update_conditions(self):
        pass

    async def tick(self):
        while True:
            await self.reactor.tick()
