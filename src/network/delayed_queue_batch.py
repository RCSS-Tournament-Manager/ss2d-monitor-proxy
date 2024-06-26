import asyncio
import logging
from src.network.delayed_queue import DelayedQueue
from src.network.proxy_queue import IQueue, QueueType


class DelayedQueueBatch(IQueue):
    def __init__(self, n=1, buffer_size=500) -> None:
        self.queue: list[IQueue] = []
        self.buffer_size = buffer_size
        for _ in range(n):
            self.queue.append(DelayedQueue(buffer_size))
        self.logger = logging.getLogger(f"DelayedQueueBatch")
    
    async def put(self, msg: str):
        put_tasks = []
        for i in range(len(self.queue)):
            put_tasks.append(asyncio.create_task(self.queue[i].put(msg)))
            
        await asyncio.gather(*put_tasks)
    
    async def get(self, i):
        return await self.queue[i].get()
    
    def size(self) -> int:
        return len(self.queue)
    
    def get_queue(self, i) -> IQueue:
        return self.queue[i]
    
    def get_type(self) -> QueueType:
        return QueueType.DELAYED