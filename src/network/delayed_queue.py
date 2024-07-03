import asyncio
from src.network.proxy_queue import IQueue
from src.network.simple_queue import SimpleQueue



class DelayedQueue(IQueue):
    def __init__(self, buffer=500) -> None:
        self.queue: IQueue = SimpleQueue()
        self.buffer_size = buffer
        self.buffer = 0

    async def put(self, msg: str):
        await self.queue.put(msg)
        self.buffer += 1

    async def get(self):
        while self.buffer < self.buffer_size:
            await asyncio.sleep(0.1)
        self.buffer -= 1
        return await self.queue.get()

    def size(self):
        return 1

    def get_queue(self, i=0) -> 'DelayedQueue':
        return self
    
    def clear(self) -> None:
        self.queue = SimpleQueue()
    