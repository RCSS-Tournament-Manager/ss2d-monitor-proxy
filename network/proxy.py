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
            logging.debug('Receiving message')
            msg = await self.receiver.receive()
            await self.queue.put(msg)
        
    async def send(self):
        while True:
            logging.debug('Sending message')
            msg = await self.queue.get()
            logging.debug('Got queue item')
            self.sender.send(msg)
    
    async def run(self) -> None:
        logging.info('Proxy started')
        # TODO INITIALIZE HERE?
        logging.info('Initializing sender and receiver')        
        self.sender.initialize()
        self.receiver.initialize()
        
        send_task = asyncio.create_task(self.send())
        receive_task = asyncio.create_task(self.receive())
        
        await send_task
        await receive_task