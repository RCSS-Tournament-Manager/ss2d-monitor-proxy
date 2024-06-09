import asyncio
from network.communication import ICom
from network.proxy_queue import IQueue


class IReceiver(ICom):
    def __init__(self) -> None:
        super().__init__()
    
    async def receive(self) -> str:
        pass
    
    def get_name(self) -> str:
        return "Receiver"
    
    async def send_dummy(self) -> None:
        while True:
            self.logging.info("Sending dummy message, to keep the connection alive")
            await self.queue.put('()')
            await asyncio.sleep(0.5)
    