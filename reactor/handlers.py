import asyncio
from reactor.events import RiseRods, LowerRods, ReactorAZ
from reactor.exceptions import HighRoadLevel, LowRoadLevel
from reactor.unit import Reactor


# TODO: Add lock


async def rise_rods(event: RiseRods) -> None:
    await asyncio.sleep(1)
    reactor: Reactor = event.unit
    if reactor.roads_level > 10:
        raise HighRoadLevel

    reactor.roads_level += 1


async def lower_rods(event: LowerRods) -> None:
    await asyncio.sleep(1)
    reactor: Reactor = event.unit

    if reactor.roads_level < 1:
        raise LowRoadLevel

    reactor.roads_level -= 1


async def stop_reactor(event: ReactorAZ) -> None:
    # TODO: Cancel other tasks
    reactor: Reactor = event.unit
    # Add some reactivity first
    for i in range(10):
        reactor.reactivity += 10
        await asyncio.sleep(0.1)

    for i in range(reactor.roads_level):
        await asyncio.sleep(1)
        reactor.roads_level -= 1