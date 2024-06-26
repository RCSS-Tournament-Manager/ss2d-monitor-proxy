import asyncio
import logging
from src.network.proxy_queue import IQueue


class SimpleQueue(IQueue):
    def __init__(self) -> None:
        self.queue = asyncio.Queue()
    
    async def put(self, msg: str):
        await self.queue.put(msg)
    
    async def get(self, i=0):
        return await self.queue.get()
    
    def size(self):
        return 1
    
    def get_queue(self, i=0) -> 'SimpleQueue':
        return self