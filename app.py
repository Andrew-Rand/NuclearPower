import asyncio
from fastapi import FastAPI

from mapper import MAPPER
from main import station
from station.reactor.router import reactor_router

app = FastAPI()


QUEUE = asyncio.Queue()


# TODO: queue to handle events
async def tick(queue: asyncio.Queue) -> None:
    while True:
        print('tick')
        await asyncio.sleep(1)
        task = await queue.get()

        print('start')

        processor = MAPPER.get(type(task))
        if processor:
            asyncio.create_task(processor(task))
            queue.task_done()

        print('finish')


async def main() -> None:
    asyncio.create_task(tick(QUEUE))
    asyncio.create_task(station.tick())
    await asyncio.gather(QUEUE.join())


@app.on_event('startup')
async def startup_event():
    asyncio.create_task(main())


app.include_router(reactor_router)
