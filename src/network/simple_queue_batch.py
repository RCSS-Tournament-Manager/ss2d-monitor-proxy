import asyncio
import logging
from src.network.proxy_queue import IQueue, QueueType
from src.network.simple_queue import SimpleQueue


class SimpleQueueBatch(IQueue):
    def __init__(self, n=1) -> None:
        self.queue: list[SimpleQueue] = []
        for _ in range(n):
            self.queue.append(SimpleQueue())
    
    async def put(self, msg: str):
        put_tasks = []
        for i in range(len(self.queue)):
            put_tasks.append(asyncio.create_task(self.queue[i].put(msg)))
            
        await asyncio.gather(*put_tasks)
    
    async def get(self, i):
        return await self.queue[i].get()
    
    def size(self) -> int:
        return len(self.queue)
    
    def get_queue(self, i) -> SimpleQueue:
        return self.queue[i]
    
    def get_type(self):
        return QueueType.SIMPLE