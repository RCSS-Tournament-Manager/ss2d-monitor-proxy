import asyncio
from network.proxy_queue import IQueue


class SimpleQueue(IQueue):
    def __init__(self) -> None:
        self.queue = asyncio.Queue()
    
    async def put(self, msg: str) -> None:
        await self.queue.put(msg)
    
    async def get(self) -> str:
        return await self.queue.get()