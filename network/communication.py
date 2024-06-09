import asyncio
from network.proxy_queue import IQueue


class ICom:
    def __init__(self) -> None:
        self.queue = None
        self.logging = None
    
    async def initialize(self, queue: IQueue) -> None:
        self.queue = queue
        
    def get_name(self) -> str:
        return "ICOM"
