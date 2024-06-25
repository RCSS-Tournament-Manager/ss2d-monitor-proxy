import asyncio
from enum import Enum
from network.proxy_queue import IQueue

class ComType(Enum):
    UDP = "UDP"
    RMQ = "RMQ"
    WS = "WS"

class ICom:
    def __init__(self) -> None:
        self.queue = None
        self.logging = None
    
    async def initialize(self, queue: IQueue) -> None:
        self.queue = queue
        
    def get_name(self) -> str:
        return "ICOM"
    
    def get_type(self) -> ComType:
        return None
