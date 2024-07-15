import asyncio
import logging
from re import I

import websockets
from src.network.communication import ComType
from src.network.proxy_queue import IQueue
from src.network.receiver_udp import MONITOR_INITIAL_MESSAGE
from src.network.sender import ISender
from src.network.simple_queue_batch import SimpleQueueBatch


class SenderWebSocket(ISender):
    def __init__(self, address: tuple[str, int]) -> None:
        super().__init__()
        self.address = address
        self.logging = logging.getLogger(f"Sender-{self.get_name()}")
        self.server_task = None
        self.connected = False
        self.semaphore = asyncio.Semaphore(1)
        self.shared_queue = SimpleQueueBatch(0)
        self.sharing_task = None

    async def send(self) -> None:
        pass
    
    async def initial_queue(self) -> IQueue:
        queue = self.shared_queue.add_queue()
        logging.info(f"Added queue")
        for msg in self.parameters_messages.split('\n'):
            await queue.put(msg)
        return queue
    
    async def sharing(self) -> None:
        while True:
            msg = await self.queue.get()
            await self.shared_queue.put(msg)
            self.check_parameters(msg)
                
    async def sender(self, websocket) -> None:
        message = await websocket.recv()
        self.logging.info(f"Received initial message: {message}")
        if not message.startswith(MONITOR_INITIAL_MESSAGE):
            self.logging.error(f"Invalid initial message: {message}, closing connection")
            return
        queue = await self.initial_queue()
        while True:
            msg = await queue.get()
            try:
                await websocket.send(msg)
            except websockets.exceptions.ConnectionClosedError:
                self.logging.error(f"Connection closed")
                self.shared_queue.remove_queue(queue)
                break

    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        self.sharing_task = asyncio.create_task(self.sharing())
        await websockets.serve(self.sender, self.address[0], self.address[1])
        self.logging.info("Server started")
            
    def get_name(self) -> str:
        return f"WS-{self.address}"
    
    def get_type(self) -> ComType:
        return ComType.WS

# json
# app folder
# websocket
# file reader