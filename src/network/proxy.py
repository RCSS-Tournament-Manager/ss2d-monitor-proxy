import asyncio
import logging
from socket import timeout
from src.network.proxy_queue import IQueue
from src.network.receiver import IReceiver
from src.network.sender import ISender


class Proxy:
    def __init__(self, receiver: IReceiver, senders: list[ISender], queue: IQueue) -> None:
        self.receiver = receiver
        self.senders = senders
        self.queue = queue
        self.logging = logging.getLogger(f"Proxy-{self.get_name()}")
        
    async def receive(self):
        while True:
            await self.receiver.receive()
            await asyncio.sleep(0.001) # TODO IS IT CORRECT?
        
    async def send(self):
        while True:
            send_tasks = []
            for sender in self.senders:
                if sender.get_name() == 'UDP-localhost-6100':
                    self.logging.info('Sending')
                send_tasks.append(asyncio.create_task(sender.send()))
            await asyncio.gather(*send_tasks)
            # await asyncio.sleep(0.001) # TODO IS IT CORRECT?
    
    async def run(self) -> None:
        assert self.queue.size() == len(self.senders)
        
        self.logging.info('Proxy started')
        # TODO INITIALIZE HERE?
        self.logging.info('Initializing sender and receiver')        

        initialization_tasks = []
        initialization_tasks.append(asyncio.create_task(self.receiver.initialize(self.queue)))
        for i, sender in enumerate(self.senders):
            initialization_tasks.append(asyncio.create_task(sender.initialize(self.queue.get_queue(i))))
        await asyncio.gather(*initialization_tasks)
        
        receive_task = asyncio.create_task(self.receive())
        send_task = asyncio.create_task(self.send())
        
        await receive_task
        await send_task
    
    def stop(): # TODO IMPLEMENT
        pass
    
    def get_name(self) -> str:
        return f"{self.receiver.get_name()}-{'-'.join([sender.get_name() for sender in self.senders])}"