import asyncio

import pydantic

REACTIVITY = 1
TEMPERATURE = 0
STEAM_PRESSURE = 0


class RiseRods(pydantic.BaseModel):
    '''lift the rods out of the reactor'''
    level: int


async def rise_rods(event: RiseRods) -> None:
    global REACTIVITY
    REACTIVITY *= event.level

MAPPER = {
    RiseRods: rise_rods,
}


async def tick(queue: asyncio.Queue) -> None:
    while True:
        global REACTIVITY
        print(REACTIVITY)
        task = await queue.get()

        await asyncio.sleep(3)

        processor = MAPPER.get(type(task))
        if processor:
            await processor(task)
        queue.task_done()


async def add_task(queue: asyncio.Queue) -> None:
    while True:
        # Example
        await asyncio.sleep(1)
        queue.put_nowait(RiseRods(level=3))



async def main():
    queue = asyncio.Queue()
    worker = asyncio.create_task(tick(queue))

    # example
    asyncio.create_task(add_task(queue))
    # ............

    await asyncio.gather(queue.join(), worker)

asyncio.run(main())