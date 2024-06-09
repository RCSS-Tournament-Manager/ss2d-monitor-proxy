import asyncio
import logging
from network.delayed_queue import DelayedQueue
from network.proxy_queue import IQueue


class DelayedQueueBatch(IQueue):
    def __init__(self, n=1, buffer_size=500) -> None:
        self.queue: list[IQueue] = []
        self.buffer_size = buffer_size
        self.buffer = 0
        for _ in range(n):
            self.queue.append(DelayedQueue())
        self.logger = logging.getLogger(f"DelayedQueueBatch")
    
    async def put(self, msg: str):
        put_tasks = []
        for i in range(len(self.queue)):
            put_tasks.append(asyncio.create_task(self.queue[i].put(msg)))
            
        await asyncio.gather(*put_tasks)
        self.buffer += 1
        self.logger.debug(f"Buffer: {self.buffer}")
    
    async def get(self, i):
        while self.buffer < self.buffer_size:
            await asyncio.sleep(0.1)
        self.buffer -= 1
        return await self.queue[i].get()
    
    def size(self) -> int:
        return len(self.queue)
    
    def get_queue(self, i) -> IQueue:
        return self.queue[i]
    
    def get_buffer_size(self) -> int:
        return self.buffer_size

    def get_buffer(self) -> int:
        return self.buffer