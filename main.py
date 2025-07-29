import asyncio
from functools import partial

import pydantic

REACTIVITY = 1
TEMPERATURE = 1
WATER_PRESSURE = 1
STEAM_PRESSURE = 1


class RiseRods(pydantic.BaseModel):
    '''lift the rods out of the reactor'''
    level: int


async def rise_rods(event: RiseRods) -> None:
    await asyncio.sleep(5)
    global REACTIVITY
    REACTIVITY *= event.level

MAPPER = {
    RiseRods: rise_rods,
}


async def tick(queue: asyncio.Queue) -> None:
    while True:
        task = await queue.get()

        print('start')

        processor = MAPPER.get(type(task))
        if processor:
            asyncio.create_task(processor(task))
            queue.task_done()
        print('finish')


async def conditions():
    global REACTIVITY
    global TEMPERATURE
    global WATER_PRESSURE
    global STEAM_PRESSURE

    while True:
        await asyncio.sleep(1)
        TEMPERATURE = REACTIVITY / WATER_PRESSURE
        STEAM_PRESSURE = TEMPERATURE * WATER_PRESSURE

        print(f'Reactivity: {REACTIVITY}, Temperature: {TEMPERATURE}, Steam pressure: {STEAM_PRESSURE}')


async def add_task(queue: asyncio.Queue) -> None:
    while True:
        # Example
        await asyncio.sleep(2)
        queue.put_nowait(RiseRods(level=2))



async def main():
    queue = asyncio.Queue()
    worker = asyncio.create_task(tick(queue))

    # example
    asyncio.create_task(add_task(queue))
    asyncio.create_task(conditions())
    # ............

    await asyncio.gather(queue.join(), worker)

asyncio.run(main())