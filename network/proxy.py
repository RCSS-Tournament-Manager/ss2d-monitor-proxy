import asyncio
import logging
from socket import timeout
from network.proxy_queue import IQueue
from network.receiver import IReceiver
from network.sender import ISender


class Proxy:
    def __init__(self, receiver: IReceiver, sender: ISender, queue: IQueue) -> None:
        self.receiver = receiver
        self.sender = sender
        self.queue = queue
        
    async def receive(self):
        while True:
            await self.receiver.receive()
            await asyncio.sleep(0.001) # TODO IS IT CORRECT?
        
    async def send(self):
        while True:
            await self.sender.send()
            # await asyncio.sleep(0.001) # TODO IS IT CORRECT?
            
    
    async def run(self) -> None:
        logging.info('Proxy started')
        # TODO INITIALIZE HERE?
        logging.info('Initializing sender and receiver')        
        await self.receiver.initialize(self.queue)
        await self.sender.initialize(self.queue)
        
        receive_task = asyncio.create_task(self.receive())
        send_task = asyncio.create_task(self.send())
        
        await receive_task
        await send_task
    
    def stop(): # TODO IMPLEMENT
        pass