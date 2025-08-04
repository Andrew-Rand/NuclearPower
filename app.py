import asyncio
import queue

from fastapi import FastAPI

from mapper import MAPPER
from reactor.events import RiseRods, ReactorAZ, LowerRods
from reactor.schemas import ReactorConditionsResponse
from reactor.unit import Reactor

app = FastAPI()


QUEUE = asyncio.Queue()
reactor = Reactor()


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
    global QUEUE
    global reactor
    queue = QUEUE
    worker = asyncio.create_task(tick(queue))
    reactor_tick = asyncio.create_task(reactor.tick())
    await asyncio.gather(queue.join())


@app.on_event('startup')
async def startup_event():
    asyncio.create_task(main())





# reactor

@app.get('/reactor/rise')
async def rise_rods():
    global QUEUE
    global reactor
    QUEUE.put_nowait(RiseRods(unit=reactor))

    return 'ok'


@app.get('/reactor/low')
async def lower_rods():
    global QUEUE
    global reactor
    QUEUE.put_nowait(LowerRods(unit=reactor))

    return 'ok'


@app.get('/reactor/conditions', response_model=ReactorConditionsResponse)
async def get_reactor_conditions():
    global reactor
    return reactor.conditions


@app.get('/reactor/az')
async def az_rods():
    global QUEUE
    global reactor

    QUEUE.put_nowait(ReactorAZ(unit=reactor))

