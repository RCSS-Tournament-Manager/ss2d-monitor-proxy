import asyncio
import logging
from network.proxy_queue import IQueue


class SimpleQueue(IQueue):
    def __init__(self) -> None:
        self.queue = asyncio.Queue()
    
    async def put(self, msg: str):
        await self.queue.put(msg)
    
    async def get(self):
        return await self.queue.get()