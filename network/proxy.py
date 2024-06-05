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
            msg = await self.receiver.receive()
            await self.queue.put(msg)
            await asyncio.sleep(0.001) # TODO IS IT CORRECT?
        
    async def send(self):
        while True:
            msg = await self.queue.get()
            self.sender.send(msg)
    
    async def run(self) -> None:
        logging.info('Proxy started')
        # TODO INITIALIZE HERE?
        logging.info('Initializing sender and receiver')        
        self.receiver.initialize()
        self.sender.initialize()
        
        receive_task = asyncio.create_task(self.receive())
        send_task = asyncio.create_task(self.send())
        
        await send_task
        await receive_task
    
    def stop(): # TODO IMPLEMENT
        pass